import pytest

from databricks.labs.remorph.intermediate.named import Named


@pytest.mark.parametrize("input_name, expected_output",
                         [("BigHTMLParser", ["big", "html", "parser"]), ("parseHTML", ["parse", "html"]),
                          ("parse HTML", ["parse", "html"]), ("parse-HTML", ["parse", "html"]),
                          ("parse--HTML", ["parse", "html"]), ("parse_HTML", ["parse", "html"]),
                          ("parseHTMLNow", ["parse", "html", "now"]), ("parseHtml", ["parse", "html"]),
                          ("ParseHtml", ["parse", "html"]), ("clusterID", ["cluster", "id"]),
                          ("positionX", ["position", "x"]), ("parseHtmlNow", ["parse", "html", "now"]),
                          ("HTMLParser", ["html", "parser"]), ("BigO", ["big", "o"]),
                          ("OCaml", ["o", "caml"]), ("K8S_FAILURE", ["k8s", "failure"]),
                          ("k8sFailure", ["k8s", "failure"]), ("i18nFailure", ["i18n", "failure"]),
                          ("Patch:Request", ["patch", "request"]),
                          ("urn:ietf:params:scim:api:messages:2.0:PatchOp",
                           ["urn", "ietf", "params", "scim", "api", "messages", "2", "0", "patch", "op"]), ])
def test_named_decamel(input_name, expected_output):
    named_instance = Named(input_name)
    assert list(named_instance._split_ascii()) == expected_output


def test_named_transforms():
    n = Named("bigBrownFOX")
    assert n.camel_name() == "bigBrownFox"
    assert n.pascal_name() == "BigBrownFox"
    assert n.constant_name() == "BIG_BROWN_FOX"
    assert n.snake_name() == "big_brown_fox"
    assert n.kebab_name() == "big-brown-fox"
    assert n.title_name() == "Big Brown Fox"
    assert n.abbr_name() == "bbf"


@pytest.mark.parametrize("input_name, expected_output", [("buses", "bus"), ("boxes", "box"),
                                                         ("branches", "branch"), ("blitzes", "blitz"),
                                                         ("cluster-policies", "cluster-policy"),
                                                         ("clusters", "cluster"), ("dbfs", "dbfs"),
                                                         ("alerts", "alert"), ("dashboards", "dashboard"),
                                                         ("data-sources", "data-source"),
                                                         ("dbsql-permissions", "dbsql-permission"),
                                                         ("queries", "query"),
                                                         ("delta-pipelines", "delta-pipeline"),
                                                         ("repos", "repo"), ("metastores", "metastore"),
                                                         ("tables", "table"), ("workspace", "workspace"),
                                                         ("warehouses", "warehouse"), ])
def test_named_singular(input_name, expected_output):
    n = Named(input_name)
    assert n.singular().kebab_name() == expected_output
