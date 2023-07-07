from typing import Iterable, List
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions
from couchbase.auth import PasswordAuthenticator
from datahub.configuration.source_common import EnvConfigMixin
from typing import Iterable, List
import logging
from dataclasses import dataclass, field
from pydantic.fields import Field
from datahub.ingestion.api.common import PipelineContext
from datahub.ingestion.api.decorators import (
    SourceCapability,
    SupportStatus,
    capability,
    config_class,
    platform_name,
    support_status,
)
from datahub.metadata.com.linkedin.pegasus2avro.metadata.snapshot import DatasetSnapshot
from datahub.metadata.schema_classes import DatasetPropertiesClass
from datahub.ingestion.api.workunit import MetadataWorkUnit
from datahub.metadata.com.linkedin.pegasus2avro.mxe import MetadataChangeEvent
from datahub.metadata.com.linkedin.pegasus2avro.schema import (
    ArrayTypeClass,
    BooleanTypeClass,
    NullTypeClass,
    NumberTypeClass,
    RecordTypeClass,
    SchemaField,
    SchemaFieldDataType,
    SchemalessClass,
    SchemaMetadata,
    StringTypeClass,
    UnionTypeClass,
)
from datahub.ingestion.api.source import Source, SourceReport
from datahub.ingestion.api.source_helpers import auto_workunit_reporter
from datahub.ingestion.api.workunit import MetadataWorkUnit

logger = logging.getLogger(__name__)

class CouchbaseConfig(EnvConfigMixin):

    connect_uri: str = Field(
        default="Couchbase://localhost"
    )
    username: str = Field(default=None,description="Couchbase Cluster username")
    password: str = Field(default=None, description= "Couchbase cluster password")


@dataclass
class CouchbaseSourceReport(SourceReport):
    filtered: List[str] = field(default_factory=list)

    def report_dropped(self, name: str) -> None:
        self.filtered.append(name)

_field_type_mapping = {
    list: ArrayTypeClass,
    bool: BooleanTypeClass,
    type(None): NullTypeClass,
    int: NumberTypeClass,
    float: NumberTypeClass,
    str: StringTypeClass,
    dict: RecordTypeClass,
    "mixed": UnionTypeClass,
}
def get_field_type(self,
        value, bucket_name: str
    ) -> SchemaFieldDataType:
        TypeClass = _field_type_mapping.get(type(value))
        if TypeClass is None:
            self.report.report_warning(
                bucket_name, f"unable to map type {value} to metadata schema"
            )
            TypeClass = NullTypeClass

        return SchemaFieldDataType(type=TypeClass())

@platform_name("couchbase")
@config_class(CouchbaseConfig)
@support_status(SupportStatus.CERTIFIED)
@capability(SourceCapability.LINEAGE_COARSE, "Enabled by default")
@dataclass
class CouchbaseSource(Source):

    config: CouchbaseConfig
    report: CouchbaseSourceReport
    couchbase_client: Cluster

    def __init__(self, ctx: PipelineContext, config: CouchbaseConfig):
        super().__init__(ctx)
        self.config = config
        self.report = CouchbaseSourceReport()

        options = {}
        if self.config.username is not None:
            options["username"] = self.config.username
        if self.config.password is not None:
            options["password"] = self.config.password

        self.couchbase_client = Cluster('couchbase://localhost',ClusterOptions(PasswordAuthenticator(self.config.username,self.config.password)))


    @classmethod
    def create(cls, config_dict: dict, ctx: PipelineContext) -> "CouchbaseSource":
        config = CouchbaseConfig.parse_obj(config_dict)
        return cls(ctx, config)


    def get_workunits(self) -> Iterable[MetadataWorkUnit]:
        return auto_workunit_reporter(self.report, self.get_workunits_internal())

    def get_workunits_internal(self) -> Iterable[MetadataWorkUnit]:
        platform = "couchbase"
        bucket_manager = self.couchbase_client.buckets()
        bucket_info = bucket_manager.get_all_buckets()
        bucket_names = [bucket.name for bucket in bucket_info]
        if bucket_info is None:
            self.report.report_warning("No buckets were found!")
        for bucket in bucket_names:
            bucket_name = bucket
            query = f'SELECT META().id FROM `{bucket_name}`'
            result = self.couchbase_client.query(query)
            for row in result:
                location = f"{bucket_name}.{row['id']}"
                dataset_urn = f"urn:li:dataset:(urn:li:dataPlatform:{platform},{location},{self.config.env})"
                dataset_snapshot = DatasetSnapshot(
                            urn=dataset_urn,
                            aspects=[],
                        )

                dataset_properties = DatasetPropertiesClass(
                    tags=[],
                    customProperties={},
                )
                dataset_snapshot.aspects.append(dataset_properties)
                canonical_schema: List[SchemaField] = []
                bucket = self.couchbase_client.bucket(f'{bucket_name}')
                collection = bucket.default_collection()
                row_Data = collection.get(row['id'])
                document = row_Data.value
                for key, value in document.items():
                    value_type = type(value)
                    dict = {key: value_type.__name__}
                    value_type = value_type.__name__
                    field = SchemaField(
                        fieldPath= key,
                        nativeDataType= value_type,
                        type=get_field_type(self,
                            value, bucket_name
                        ),
                        description=None,
                        recursive=False,
                    )
                    canonical_schema.append(field)  


            schema_metadata = SchemaMetadata(
                schemaName=bucket_name,
                platform=f"urn:li:dataPlatform:{platform}",
                version=0,
                hash="",
                platformSchema=SchemalessClass(),
                fields=canonical_schema,
            )

            dataset_snapshot.aspects.append(schema_metadata)

            mce = MetadataChangeEvent(proposedSnapshot=dataset_snapshot)
            yield MetadataWorkUnit(id=bucket_name, mce=mce)
        


    def get_report(self) -> CouchbaseSourceReport:
        return self.report

    def close(self):
        self.couchbase_client.close()
        super().close()


