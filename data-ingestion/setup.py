import os
import sys
from typing import Dict, Set

import setuptools

package_metadata: dict = {}
with open("./src/datahub/__init__.py") as fp:
    exec(fp.read(), package_metadata)


def get_long_description():
    root = os.path.dirname(__file__)
    with open(os.path.join(root, "README.md")) as f:
        description = f.read()

    return description


base_requirements = {
    # Typing extension should be >=3.10.0.2 ideally but we can't restrict due to Airflow 2.0.2 dependency conflict
    "typing_extensions>=3.7.4.3 ;  python_version < '3.8'",
    "typing_extensions>=3.10.0.2 ;  python_version >= '3.8'",
    "mypy_extensions>=0.4.3",
    # Actual dependencies.
    "typing-inspect",
    # pydantic 1.10.3 is incompatible with typing-extensions 4.1.1 - https://github.com/pydantic/pydantic/issues/4885
    "pydantic>=1.5.1,!=1.10.3",
    "mixpanel>=4.9.0",
}

framework_common = {
    "jsonschema",
    "py4j",
    "click>=7.1.2",
    "click-default-group",
    "sqlalchemy>=1.3.24, <2",
}

rest_common = {"requests", "requests_file"}

sql_common = {
    # Required for all SQL sources.
    "sqlalchemy>=1.3.24, <2",
}

sqllineage_lib = "sqllineage==1.3.6"

aws_common = {
    # AWS Python SDK
    "boto3",
    # Deal with a version incompatibility between botocore (used by boto3) and urllib3.
    # See https://github.com/boto/botocore/pull/2563.
    "botocore!=1.23.0",
}

base_dev_requirements = {
    *base_requirements,
    *framework_common,
}

dev_requirements = {
    *base_dev_requirements,
    # Extra requirements for Airflow.
    "virtualenv",  # needed by PythonVirtualenvOperator
}

entry_points = {
    "console_scripts": ["nt = datahub.entrypoints:main","test = datahub.entrypoints:test"],
    "datahub.ingestion.source.plugins": [
        "csv-enricher = datahub.ingestion.source.csv_enricher:CSVEnricherSource",
        "file = datahub.ingestion.source.file:GenericFileSource",
        "sqlalchemy = datahub.ingestion.source.sql.sql_generic:SQLAlchemyGenericSource",
        "athena = datahub.ingestion.source.sql.athena:AthenaSource",
        "azure-ad = datahub.ingestion.source.identity.azure_ad:AzureADSource",
        "bigquery = datahub.ingestion.source.bigquery_v2.bigquery:BigqueryV2Source",
        "clickhouse = datahub.ingestion.source.sql.clickhouse:ClickHouseSource",
        "clickhouse-usage = datahub.ingestion.source.usage.clickhouse_usage:ClickHouseUsageSource",
        "delta-lake = datahub.ingestion.source.delta_lake:DeltaLakeSource",
        "s3 = datahub.ingestion.source.s3:S3Source",
        "dbt = datahub.ingestion.source.dbt.dbt_core:DBTCoreSource",
        "dbt-cloud = datahub.ingestion.source.dbt.dbt_cloud:DBTCloudSource",
        "druid = datahub.ingestion.source.sql.druid:DruidSource",
        "elasticsearch = datahub.ingestion.source.elastic_search:ElasticsearchSource",
        "feast = datahub.ingestion.source.feast:FeastRepositorySource",
        "glue = datahub.ingestion.source.aws.glue:GlueSource",
        "sagemaker = datahub.ingestion.source.aws.sagemaker:SagemakerSource",
        "hana = datahub.ingestion.source.sql.hana:HanaSource",
        "hive = datahub.ingestion.source.sql.hive:HiveSource",
        "json-schema = datahub.ingestion.source.schema.json_schema:JsonSchemaSource",
        "kafka = datahub.ingestion.source.kafka:KafkaSource",
        "kafka-connect = datahub.ingestion.source.kafka_connect:KafkaConnectSource",
        "ldap = datahub.ingestion.source.ldap:LDAPSource",
        "looker = datahub.ingestion.source.looker.looker_source:LookerDashboardSource",
        "lookml = datahub.ingestion.source.looker.lookml_source:LookMLSource",
        "datahub-lineage-file = datahub.ingestion.source.metadata.lineage:LineageFileSource",
        "datahub-business-glossary = datahub.ingestion.source.metadata.business_glossary:BusinessGlossaryFileSource",
        "mode = datahub.ingestion.source.mode:ModeSource",
        "mongodb = datahub.ingestion.source.mongodb:MongoDBSource",
        "mssql = datahub.ingestion.source.sql.mssql:SQLServerSource",
        "mysql = datahub.ingestion.source.sql.mysql:MySQLSource",
        "mariadb = datahub.ingestion.source.sql.mariadb.MariaDBSource",
        "okta = datahub.ingestion.source.identity.okta:OktaSource",
        "oracle = datahub.ingestion.source.sql.oracle:OracleSource",
        "postgres = datahub.ingestion.source.sql.postgres:PostgresSource",
        "redash = datahub.ingestion.source.redash:RedashSource",
        "redshift = datahub.ingestion.source.sql.redshift:RedshiftSource",
        "redshift-usage = datahub.ingestion.source.usage.redshift_usage:RedshiftUsageSource",
        "snowflake = datahub.ingestion.source.snowflake.snowflake_v2:SnowflakeV2Source",
        "superset = datahub.ingestion.source.superset:SupersetSource",
        "tableau = datahub.ingestion.source.tableau:TableauSource",
        "openapi = datahub.ingestion.source.openapi:OpenApiSource",
        "metabase = datahub.ingestion.source.metabase:MetabaseSource",
        "trino = datahub.ingestion.source.sql.trino:TrinoSource",
        "starburst-trino-usage = datahub.ingestion.source.usage.starburst_trino_usage:TrinoUsageSource",
        "nifi = datahub.ingestion.source.nifi:NifiSource",
        "powerbi = datahub.ingestion.source.powerbi:PowerBiDashboardSource",
        "powerbi-report-server = datahub.ingestion.source.powerbi_report_server:PowerBiReportServerDashboardSource",
        "iceberg = datahub.ingestion.source.iceberg.iceberg:IcebergSource",
        "vertica = datahub.ingestion.source.sql.vertica:VerticaSource",
        "presto = datahub.ingestion.source.sql.presto:PrestoSource",
        "presto-on-hive = datahub.ingestion.source.sql.presto_on_hive:PrestoOnHiveSource",
        "pulsar = datahub.ingestion.source.pulsar:PulsarSource",
        "salesforce = datahub.ingestion.source.salesforce:SalesforceSource",
        "demo-data = datahub.ingestion.source.demo_data.DemoDataSource",
        "unity-catalog = datahub.ingestion.source.unity.source:UnityCatalogSource",
    ],
    "datahub.ingestion.transformer.plugins": [
        "simple_remove_dataset_ownership = datahub.ingestion.transformer.remove_dataset_ownership:SimpleRemoveDatasetOwnership",
        "mark_dataset_status = datahub.ingestion.transformer.mark_dataset_status:MarkDatasetStatus",
        "set_dataset_browse_path = datahub.ingestion.transformer.add_dataset_browse_path:AddDatasetBrowsePathTransformer",
        "add_dataset_ownership = datahub.ingestion.transformer.add_dataset_ownership:AddDatasetOwnership",
        "simple_add_dataset_ownership = datahub.ingestion.transformer.add_dataset_ownership:SimpleAddDatasetOwnership",
        "pattern_add_dataset_ownership = datahub.ingestion.transformer.add_dataset_ownership:PatternAddDatasetOwnership",
        "add_dataset_domain = datahub.ingestion.transformer.dataset_domain:AddDatasetDomain",
        "simple_add_dataset_domain = datahub.ingestion.transformer.dataset_domain:SimpleAddDatasetDomain",
        "pattern_add_dataset_domain = datahub.ingestion.transformer.dataset_domain:PatternAddDatasetDomain",
        "add_dataset_tags = datahub.ingestion.transformer.add_dataset_tags:AddDatasetTags",
        "simple_add_dataset_tags = datahub.ingestion.transformer.add_dataset_tags:SimpleAddDatasetTags",
        "pattern_add_dataset_tags = datahub.ingestion.transformer.add_dataset_tags:PatternAddDatasetTags",
        "add_dataset_terms = datahub.ingestion.transformer.add_dataset_terms:AddDatasetTerms",
        "simple_add_dataset_terms = datahub.ingestion.transformer.add_dataset_terms:SimpleAddDatasetTerms",
        "pattern_add_dataset_terms = datahub.ingestion.transformer.add_dataset_terms:PatternAddDatasetTerms",
        "add_dataset_properties = datahub.ingestion.transformer.add_dataset_properties:AddDatasetProperties",
        "simple_add_dataset_properties = datahub.ingestion.transformer.add_dataset_properties:SimpleAddDatasetProperties",
        "pattern_add_dataset_schema_terms = datahub.ingestion.transformer.add_dataset_schema_terms:PatternAddDatasetSchemaTerms",
        "pattern_add_dataset_schema_tags = datahub.ingestion.transformer.add_dataset_schema_tags:PatternAddDatasetSchemaTags",
    ],
    "datahub.ingestion.sink.plugins": [
        "file = datahub.ingestion.sink.file:FileSink",
        "console = datahub.ingestion.sink.console:ConsoleSink",
        "blackhole = datahub.ingestion.sink.blackhole:BlackHoleSink",
        "datahub-kafka = datahub.ingestion.sink.datahub_kafka:DatahubKafkaSink",
        "datahub-rest = datahub.ingestion.sink.datahub_rest:DatahubRestSink",
        "datahub-lite = datahub.ingestion.sink.datahub_lite:DataHubLiteSink",
    ],
    "datahub.ingestion.checkpointing_provider.plugins": [
        "datahub = datahub.ingestion.source.state_provider.datahub_ingestion_checkpointing_provider:DatahubIngestionCheckpointingProvider",
    ],
    "datahub.ingestion.reporting_provider.plugins": [
        "datahub = datahub.ingestion.reporting.datahub_ingestion_run_summary_provider:DatahubIngestionRunSummaryProvider",
        "file = datahub.ingestion.reporting.file_reporter:FileReporter",
    ],
    "apache_airflow_provider": ["provider_info=datahub_provider:get_provider_info"],
}


setuptools.setup(
    # Package metadata.
    name=package_metadata["__package_name__"],
    version=package_metadata["__version__"],
    url="https://datahubproject.io/",
    project_urls={
        "Documentation": "https://datahubproject.io/docs/",
        "Source": "https://github.com/datahub-project/datahub",
        "Changelog": "https://github.com/datahub-project/datahub/releases",
    },
    license="Apache License 2.0",
    description="A CLI to work with DataHub metadata",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Unix",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Topic :: Software Development",
    ],
    # Package info.
    zip_safe=False,
    python_requires=">=3.7",
    package_dir={"": "src"},
    packages=setuptools.find_namespace_packages(where="./src"),
    package_data={
        "datahub": ["py.typed"],
        "datahub.metadata": ["schema.avsc"],
        "datahub.metadata.schemas": ["*.avsc"],
        "datahub.ingestion.source.powerbi": ["powerbi-lexical-grammar.rule"],
    },
    entry_points=entry_points,
    # Dependencies.
    install_requires=list(base_requirements | framework_common),
    extras_require={
        "base": list(framework_common),
        "dev": list(dev_requirements),
    },
)
