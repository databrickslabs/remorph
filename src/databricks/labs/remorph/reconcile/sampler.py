import logging
from abc import ABC, abstractmethod

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from databricks.labs.remorph.reconcile.constants import SamplingOptionMethod, SamplingSpecificationsType
from databricks.labs.remorph.reconcile.recon_config import SamplingOptions, SamplingSpecifications

logger = logging.getLogger(__name__)

_MIN_SAMPLE_COUNT = 50
_MAX_SAMPLE_COUNT = 400

_MIN_BUCKET_LIMIT = 2
_MAX_BUCKET_LIMIT = 50


class Sampler(ABC):
    def __init__(
        self,
        sampling_options: SamplingOptions
    ):
        self._sampling_options = sampling_options

    @abstractmethod
    def _validate_sampling_options(self):
        return NotImplemented

    @abstractmethod
    def sample(
        self,
        keys_df : DataFrame,
        key_columns: list[str],
        target_table: DataFrame,
    ) -> DataFrame:
        return NotImplemented


class RandomSampler(Sampler):
    def __init__(self, sampling_options: SamplingOptions, seed: int = 100):
        super().__init__(sampling_options)
        self.seed = seed

    def _validate_sampling_options(self):
        if self._sampling_options.method != SamplingOptionMethod.RANDOM:
            raise ValueError("RandomSampler: Only 'random' sampling method is supported")

        specs = self._sampling_options.specifications
        if specs.type == SamplingSpecificationsType.FRACTION and (specs.value is None or (not 0 < specs.value < 1)):
            raise ValueError("RandomSampler: Fraction value must be greater than  0 and less than 1")

        if specs.type == SamplingSpecificationsType.COUNT and (specs.value is None or (specs.value < _MIN_SAMPLE_COUNT)):
            logger.info(f"RandomSampler: Sample count must be >= {_MIN_SAMPLE_COUNT}, "
                           f"flooring to {_MIN_SAMPLE_COUNT}")
            self._sampling_options.specifications.value = _MIN_SAMPLE_COUNT

        elif specs.type == SamplingSpecificationsType.COUNT and specs.value > _MAX_SAMPLE_COUNT:
            logger.info(f"RandomSampler: Sample count must be <= {_MAX_SAMPLE_COUNT}, "
                           f"capping to {_MAX_SAMPLE_COUNT}")
            self._sampling_options.specifications.value = _MAX_SAMPLE_COUNT

    def sample(
        self,
        keys_df: DataFrame,
        key_columns: list[str],
        target_table: DataFrame
    ) -> DataFrame:

        self._validate_sampling_options()
        specs = self._sampling_options.specifications
        sampled_df = None

        if specs.type == SamplingSpecificationsType.FRACTION:
            sampled_df = keys_df.sample(fraction=specs.value, seed=self.seed)
        if specs.type == SamplingSpecificationsType.COUNT:
            total_count = keys_df.count()
            sample_size = int(specs.value)
            fraction = min(1.0, sample_size / total_count)
            sampled_df = keys_df.sample(fraction=fraction, seed=self.seed).limit(sample_size)

        return sampled_df


class StratifiedSampler(Sampler):
    def __init__(self, sampling_options: SamplingOptions, seed: int = 100):
        super().__init__(sampling_options)
        self.seed = seed

    def _validate_sampling_options(self):
        if self._sampling_options.method != SamplingOptionMethod.STRATIFIED:
            raise ValueError("StratifiedSampler: Only 'stratified' sampling method is supported")

        specs = self._sampling_options.specifications
        stratified_buckets = self._sampling_options.stratified_buckets

        if specs.type == SamplingSpecificationsType.FRACTION and (specs.value is None or (not 0 < specs.value < 1)):
            raise ValueError("StratifiedSampler: Fraction value must be greater than  0 and less than 1")

        if specs.type == SamplingSpecificationsType.COUNT and (specs.value is None or (specs.value < _MIN_SAMPLE_COUNT)):
            logger.info(f"StratifiedSampler: Sample count must be >= {_MIN_SAMPLE_COUNT}, "
                        f"flooring to {_MIN_SAMPLE_COUNT}")
            self._sampling_options.specifications.value = _MIN_SAMPLE_COUNT

        elif specs.type == SamplingSpecificationsType.COUNT and specs.value > _MAX_SAMPLE_COUNT:
            logger.info(f"StratifiedSampler: Sample count must be <= {_MAX_SAMPLE_COUNT}, "
                        f"capping to {_MAX_SAMPLE_COUNT}")
            self._sampling_options.specifications.value = _MAX_SAMPLE_COUNT

        if stratified_buckets < _MIN_BUCKET_LIMIT:
            logger.info(f"StratifiedSampler: Stratified buckets must be >= {_MIN_BUCKET_LIMIT}, "
                           f"flooring to {_MIN_BUCKET_LIMIT}")
            self._sampling_options.stratified_buckets = _MIN_BUCKET_LIMIT
        elif stratified_buckets > _MAX_BUCKET_LIMIT:
            logger.info(f"StratifiedSampler: Stratified buckets must be <= {_MAX_BUCKET_LIMIT}, "
                           f"capping to {_MAX_BUCKET_LIMIT}")
            self._sampling_options.stratified_buckets = _MAX_BUCKET_LIMIT

    def sample(
        self,
        keys_df: DataFrame,
        key_columns: list[str],
        target_table: DataFrame
    ) -> DataFrame:

        self._validate_sampling_options()

        specs = self._sampling_options.specifications
        stratified_columns = self._sampling_options.stratified_columns
        non_key_stratified_columns = [col for col in self._sampling_options.stratified_columns if col not in key_columns]
        stratified_buckets = self._sampling_options.stratified_buckets

        keys_df.select(*key_columns)
        sampled_df = None
        # Join the mismatched_df with target_table_df
        joined_df = keys_df.join(target_table, [keys_df[col] == target_table[col] for col in key_columns], "inner") \
            .select(*[keys_df[col] for col in key_columns], *[target_table[col] for col in non_key_stratified_columns])

        # Create a hash bucket column based on the stratified columns
        hash_col = F.abs(F.hash(*stratified_columns))
        bucket_col = F.pmod(hash_col,stratified_buckets).alias("bucket")

        # Add the bucket column to the joined_df
        bucketed_df = joined_df.withColumn("bucket", bucket_col)

        if specs.type == SamplingSpecificationsType.FRACTION:
            # Calculate fractions for each bucket
            unique_values = bucketed_df.select("bucket").distinct().collect()
            fractions = {row["bucket"]: specs.value for row in unique_values}
            sampled_df = bucketed_df.sampleBy("bucket", fractions=fractions, seed=self.seed)

        elif specs.type == SamplingSpecificationsType.COUNT:
            # Calculate fractions for each bucket
            sample_size = int(specs.value)
            bucket_counts = bucketed_df.groupBy("bucket").count().collect()
            total_count = sum(row['count'] for row in bucket_counts)
            fractions = {row["bucket"]: min(1.0, ( specs.value * row['count'] / total_count) / row['count']) for row
                         in bucket_counts}
            sampled_df = bucketed_df.sampleBy("bucket", fractions=fractions, seed=self.seed).limit(sample_size)

        return sampled_df.select(*key_columns)


class SamplerFactory:
    @staticmethod
    def get_sampler(sampling_options: SamplingOptions = None, seed: int = 100) -> Sampler:
        # If no sampling options provided, use default
        if sampling_options is None:
            default_sampling_options = SamplingOptions(
                method=SamplingOptionMethod.RANDOM,
                specifications=SamplingSpecifications(type=SamplingSpecificationsType.COUNT, value=100),
                stratified_columns=None,
                stratified_buckets=None
            )
            logger.info(f"SamplerFactory: No sampling options provided, using default options: "
                           f"{default_sampling_options}")
            sampling_options = default_sampling_options


        else :
            logger.info(f"SamplerFactory: Creating sampler using provided options: "
                           f"{sampling_options}")

        # Use a dictionary-based dispatch for better extensibility
        sampler_map = {
            SamplingOptionMethod.RANDOM: RandomSampler,
            SamplingOptionMethod.STRATIFIED: StratifiedSampler
        }

        # Get the sampler class
        sampler_class = sampler_map.get(
            sampling_options.method
        )

        return sampler_class(sampling_options, seed)




