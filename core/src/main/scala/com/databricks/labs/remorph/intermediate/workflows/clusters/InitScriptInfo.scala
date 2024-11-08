package com.databricks.labs.remorph.intermediate.workflows.clusters

import com.databricks.labs.remorph.intermediate.workflows.sources.{Adlsgen2Info, DbfsStorageInfo, GcsStorageInfo, LocalFileInfo, S3StorageInfo, VolumesStorageInfo, WorkspaceStorageInfo}
import com.databricks.labs.remorph.intermediate.workflows._
import com.databricks.sdk.service.compute

case class InitScriptInfo(
    abfss: Option[Adlsgen2Info] = None,
    dbfs: Option[DbfsStorageInfo] = None,
    file: Option[LocalFileInfo] = None,
    gcs: Option[GcsStorageInfo] = None,
    s3: Option[S3StorageInfo] = None,
    volumes: Option[VolumesStorageInfo] = None,
    workspace: Option[WorkspaceStorageInfo] = None)
    extends JobNode {
  override def children: Seq[JobNode] = Seq() ++ abfss ++ dbfs ++ file ++ gcs ++ s3 ++ volumes ++ workspace
  def toSDK: compute.InitScriptInfo = new compute.InitScriptInfo()
    .setAbfss(abfss.map(_.toSDK).orNull)
    .setDbfs(dbfs.map(_.toSDK).orNull)
    .setFile(file.map(_.toSDK).orNull)
    .setGcs(gcs.map(_.toSDK).orNull)
    .setS3(s3.map(_.toSDK).orNull)
    .setVolumes(volumes.map(_.toSDK).orNull)
    .setWorkspace(workspace.map(_.toSDK).orNull)
}
