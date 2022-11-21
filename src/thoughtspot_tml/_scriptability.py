import warnings
from dataclasses import dataclass
from typing import Dict, List
import betterproto


class FormatConfigCategoryType(betterproto.Enum):
    NUMBER = 1
    PERCENTAGE = 2
    CURRENCY = 3
    CUSTOM = 4


class FormatConfigUnit(betterproto.Enum):
    NONE = 1
    THOUSANDS = 2
    MILLION = 3
    BILLION = 4
    TRILLION = 5
    AUTO = 6


class FormatConfigNegativeValueFormat(betterproto.Enum):
    PREFIX_DASH = 1
    SUFFIX_DASH = 2
    BRACES_NODASH = 3


@dataclass(eq=False, repr=False)
class FormatConfig(betterproto.Message):
    category: "FormatConfigCategoryType" = betterproto.enum_field(1, optional=True)
    numberFormatConfig: "FormatConfigNumberFormatConfig" = betterproto.message_field(
        2, group="formatConfigDetails", optional=True
    )
    percentageFormatConfig: "FormatConfigPercentageFormatConfig" = betterproto.message_field(
        3, group="formatConfigDetails", optional=True
    )
    currencyFormatConfig: "FormatConfigCurrencyFormatConfig" = betterproto.message_field(
        4, group="formatConfigDetails", optional=True
    )
    customFormatConfig: "FormatConfigCustomFormatConfig" = betterproto.message_field(
        5, group="formatConfigDetails", optional=True
    )
    isCategoryEditable: bool = betterproto.bool_field(6, optional=True)


@dataclass(eq=False, repr=False)
class FormatConfigNumberFormatConfig(betterproto.Message):
    unit: "FormatConfigUnit" = betterproto.enum_field(1, optional=True)
    decimals: float = betterproto.double_field(2, optional=True)
    negativeValueFormat: "FormatConfigNegativeValueFormat" = betterproto.enum_field(3, optional=True)
    toSeparateThousands: bool = betterproto.bool_field(4, optional=True)
    removeTrailingZeroes: bool = betterproto.bool_field(5, optional=True)


@dataclass(eq=False, repr=False)
class FormatConfigPercentageFormatConfig(betterproto.Message):
    decimals: float = betterproto.double_field(1, optional=True)
    removeTrailingZeroes: bool = betterproto.bool_field(2, optional=True)


@dataclass(eq=False, repr=False)
class FormatConfigCurrencyFormatConfig(betterproto.Message):
    locale: str = betterproto.string_field(1, optional=True)
    unit: "FormatConfigUnit" = betterproto.enum_field(2, optional=True)
    decimals: float = betterproto.double_field(3, optional=True)
    toSeparateThousands: bool = betterproto.bool_field(5, optional=True)
    removeTrailingZeroes: bool = betterproto.bool_field(6, optional=True)


@dataclass(eq=False, repr=False)
class FormatConfigCustomFormatConfig(betterproto.Message):
    format: str = betterproto.string_field(1, optional=True)


@dataclass(eq=False, repr=False)
class KeyValueStr(betterproto.Message):
    key: str = betterproto.string_field(1, optional=True)
    value: str = betterproto.string_field(2, optional=True)


@dataclass(eq=False, repr=False)
class ColumnProperties(betterproto.Message):
    column_type: str = betterproto.string_field(1, optional=True)
    aggregation: str = betterproto.string_field(2, optional=True)
    index_type: str = betterproto.string_field(3, optional=True)
    index_priority: float = betterproto.double_field(4, optional=True)
    synonyms: List[str] = betterproto.string_field(5, optional=True)
    is_attribution_dimension: bool = betterproto.bool_field(6, optional=True)
    is_additive: bool = betterproto.bool_field(7, optional=True)
    calendar: str = betterproto.string_field(8, optional=True)
    format_pattern: str = betterproto.string_field(9, optional=True)
    currency_type: "ColumnPropertiesCurrencyFormat" = betterproto.message_field(10, optional=True)
    is_hidden: bool = betterproto.bool_field(11, optional=True)
    geo_config: "ColumnPropertiesGeoConfigProto" = betterproto.message_field(12, optional=True)
    spotiq_preference: str = betterproto.string_field(13, optional=True)
    search_iq_preferred: bool = betterproto.bool_field(14, optional=True)
    hierarchical_column_name: str = betterproto.string_field(15, optional=True)


@dataclass(eq=False, repr=False)
class ColumnPropertiesCurrencyFormat(betterproto.Message):
    is_browser: bool = betterproto.bool_field(1, optional=True)
    column: str = betterproto.string_field(2, optional=True)
    iso_code: str = betterproto.string_field(3, optional=True)


@dataclass(eq=False, repr=False)
class ColumnPropertiesGeoConfigProto(betterproto.Message):
    latitude: bool = betterproto.bool_field(1, optional=True)
    longitude: bool = betterproto.bool_field(2, optional=True)
    country: bool = betterproto.bool_field(3, optional=True)
    region_name: "ColumnPropertiesGeoConfigProtoSubRegion" = betterproto.message_field(4, optional=True)


@dataclass(eq=False, repr=False)
class ColumnPropertiesGeoConfigProtoSubRegion(betterproto.Message):
    country: str = betterproto.string_field(1, optional=True)
    region_name: str = betterproto.string_field(2, optional=True)


@dataclass(eq=False, repr=False)
class FormulaProperties(betterproto.Message):
    column_type: str = betterproto.string_field(1, optional=True)
    aggregation: str = betterproto.string_field(3, optional=True)


@dataclass(eq=False, repr=False)
class Formula(betterproto.Message):
    id: str = betterproto.string_field(1, optional=True)
    name: str = betterproto.string_field(2, optional=True)
    expr: str = betterproto.string_field(3, optional=True)
    properties: "FormulaProperties" = betterproto.message_field(4, optional=True)
    was_auto_generated: bool = betterproto.bool_field(5, optional=True)


@dataclass(eq=False, repr=False)
class Parameter(betterproto.Message):
    id: str = betterproto.string_field(1, optional=True)
    name: str = betterproto.string_field(2, optional=True)
    data_type: str = betterproto.string_field(3, optional=True)
    default_value: str = betterproto.string_field(4, optional=True)
    list_config: "ParameterListConfig" = betterproto.message_field(5, group="value_restrictions", optional=True)
    list_column_id: str = betterproto.string_field(6, group="value_restrictions", optional=True)
    range_config: "ParameterRangeConfig" = betterproto.message_field(7, group="value_restrictions", optional=True)


@dataclass(eq=False, repr=False)
class ParameterListConfig(betterproto.Message):
    list_choice: List["ParameterListConfigListChoice"] = betterproto.message_field(1, optional=True)


@dataclass(eq=False, repr=False)
class ParameterListConfigListChoice(betterproto.Message):
    value: str = betterproto.string_field(1, optional=True)
    display_name: str = betterproto.string_field(2, optional=True)


@dataclass(eq=False, repr=False)
class ParameterRangeConfig(betterproto.Message):
    range_min: str = betterproto.string_field(1, optional=True)
    range_max: str = betterproto.string_field(2, optional=True)
    include_min: bool = betterproto.bool_field(3, optional=True)
    include_max: bool = betterproto.bool_field(4, optional=True)


@dataclass(eq=False, repr=False)
class Filter(betterproto.Message):
    column: List[str] = betterproto.string_field(1, optional=True)
    oper: str = betterproto.string_field(2, optional=True)
    values: List[str] = betterproto.string_field(3, optional=True)
    excluded_visualizations: List[str] = betterproto.string_field(4, optional=True)
    is_mandatory: bool = betterproto.bool_field(5, optional=True)


@dataclass(eq=False, repr=False)
class Join(betterproto.Message):
    id: str = betterproto.string_field(1, optional=True)
    name: str = betterproto.string_field(2, optional=True)
    source: str = betterproto.string_field(3, optional=True)
    destination: str = betterproto.string_field(4, optional=True)
    type: str = betterproto.string_field(6, optional=True)
    is_one_to_one: bool = betterproto.bool_field(7, optional=True)


@dataclass(eq=False, repr=False)
class RelationEDocProto(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    description: str = betterproto.string_field(2, optional=True)
    source: "Identity" = betterproto.message_field(3, optional=True)
    destination: "Identity" = betterproto.message_field(4, optional=True)
    on: str = betterproto.string_field(5, optional=True)
    type: str = betterproto.string_field(6, optional=True)
    is_one_to_one: bool = betterproto.bool_field(7, optional=True)


@dataclass(eq=False, repr=False)
class TablePath(betterproto.Message):
    id: str = betterproto.string_field(1, optional=True)
    table: str = betterproto.string_field(2, optional=True)
    join_path: List["TablePathJoinPath"] = betterproto.message_field(3, optional=True)


@dataclass(eq=False, repr=False)
class TablePathJoinPath(betterproto.Message):
    join: List[str] = betterproto.string_field(1, optional=True)


@dataclass(eq=False, repr=False)
class Identity(betterproto.Message):
    id: str = betterproto.string_field(1, optional=True)
    name: str = betterproto.string_field(2, optional=True)
    fqn: str = betterproto.string_field(3, optional=True)


@dataclass(eq=False, repr=False)
class WorksheetEDocProto(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    description: str = betterproto.string_field(2, optional=True)
    tables: List["Identity"] = betterproto.message_field(3, optional=True)
    joins: List["Join"] = betterproto.message_field(4, optional=True)
    table_paths: List["TablePath"] = betterproto.message_field(5, optional=True)
    formulas: List["Formula"] = betterproto.message_field(6, optional=True)
    filters: List["Filter"] = betterproto.message_field(7, optional=True)
    worksheet_columns: List["WorksheetEDocProtoWorksheetColumn"] = betterproto.message_field(8, optional=True)
    properties: "WorksheetEDocProtoQueryProperties" = betterproto.message_field(9, optional=True)
    joins_with: List["RelationEDocProto"] = betterproto.message_field(10, optional=True)
    lesson_plans: List["LessonPlanEDocProto"] = betterproto.message_field(12, optional=True)
    parameters: List["Parameter"] = betterproto.message_field(13, optional=True)


@dataclass(eq=False, repr=False)
class WorksheetEDocProtoQueryProperties(betterproto.Message):
    is_bypass_rls: bool = betterproto.bool_field(1, optional=True)
    join_progressive: bool = betterproto.bool_field(2, optional=True)


@dataclass(eq=False, repr=False)
class WorksheetEDocProtoWorksheetColumn(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    description: str = betterproto.string_field(2, optional=True)
    column_id: str = betterproto.string_field(3, optional=True)
    formula_id: str = betterproto.string_field(4, optional=True)
    properties: "ColumnProperties" = betterproto.message_field(5, optional=True)


@dataclass(eq=False, repr=False)
class LessonPlanEDocProto(betterproto.Message):
    lesson_id: int = betterproto.int32_field(1, optional=True)
    lesson_plan_string: str = betterproto.string_field(2, optional=True)


@dataclass(eq=False, repr=False)
class ViewEDocProto(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    description: str = betterproto.string_field(2, optional=True)
    tables: List["Identity"] = betterproto.message_field(3, optional=True)
    joins: List["Join"] = betterproto.message_field(4, optional=True)
    table_paths: List["TablePath"] = betterproto.message_field(5, optional=True)
    formulas: List["Formula"] = betterproto.message_field(6, optional=True)
    search_query: str = betterproto.string_field(7, optional=True)
    view_columns: List["ViewEDocProtoViewColumn"] = betterproto.message_field(8, optional=True)
    joins_with: List["RelationEDocProto"] = betterproto.message_field(9, optional=True)
    parameters: List["Parameter"] = betterproto.message_field(10, optional=True)


@dataclass(eq=False, repr=False)
class ViewEDocProtoViewColumn(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    description: str = betterproto.string_field(2, optional=True)
    search_output_column: str = betterproto.string_field(3, optional=True)
    properties: "ColumnProperties" = betterproto.message_field(4, optional=True)


@dataclass(eq=False, repr=False)
class ConnectionDoc(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    type: str = betterproto.string_field(2, optional=True)
    authentication_type: str = betterproto.string_field(3, optional=True)
    properties: List["KeyValueStr"] = betterproto.message_field(4, optional=True)
    table: List["ConnectionDocTableDoc"] = betterproto.message_field(5, optional=True)


@dataclass(eq=False, repr=False)
class ConnectionDocTableDoc(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    id: str = betterproto.string_field(2, optional=True)
    external_table: "ConnectionDocTableDocExternalTableMapping" = betterproto.message_field(3, optional=True)
    column: List["ConnectionDocTableDocColumnDoc"] = betterproto.message_field(4, optional=True)


@dataclass(eq=False, repr=False)
class ConnectionDocTableDocExternalTableMapping(betterproto.Message):
    db_name: str = betterproto.string_field(1, optional=True)
    schema_name: str = betterproto.string_field(2, optional=True)
    table_name: str = betterproto.string_field(3, optional=True)


@dataclass(eq=False, repr=False)
class ConnectionDocTableDocColumnDoc(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    id: str = betterproto.string_field(2, optional=True)
    data_type: str = betterproto.string_field(3, optional=True)
    external_column: str = betterproto.string_field(4, optional=True)


@dataclass(eq=False, repr=False)
class ConditionalFormattingProto(betterproto.Message):
    rule: List["ConditionalFormattingProtoRule"] = betterproto.message_field(1, optional=True)


@dataclass(eq=False, repr=False)
class ConditionalFormattingProtoRange(betterproto.Message):
    min: float = betterproto.double_field(1, optional=True)
    max: float = betterproto.double_field(2, optional=True)


@dataclass(eq=False, repr=False)
class ConditionalFormattingProtoRule(betterproto.Message):
    range: "ConditionalFormattingProtoRange" = betterproto.message_field(1, optional=True)
    color: str = betterproto.string_field(2, optional=True)
    plot_as_band: bool = betterproto.bool_field(5, optional=True)


@dataclass(eq=False, repr=False)
class TableVisualization(betterproto.Message):
    table_columns: List["TableVisualizationTableColumn"] = betterproto.message_field(1, optional=True)
    ordered_column_ids: List[str] = betterproto.string_field(2, optional=True)
    show_grid_summary: bool = betterproto.bool_field(3, optional=True)
    show_table_footer: bool = betterproto.bool_field(4, optional=True)
    wrap_table_header: bool = betterproto.bool_field(5, optional=True)
    client_state: str = betterproto.string_field(6, optional=True)
    client_state_v2: str = betterproto.string_field(7, optional=True)


@dataclass(eq=False, repr=False)
class TableVisualizationTableColumn(betterproto.Message):
    column_id: str = betterproto.string_field(1, optional=True)
    conditional_formatting: "ConditionalFormattingProto" = betterproto.message_field(2, optional=True)
    wrap_column_text: bool = betterproto.bool_field(4, optional=True)
    column_width: int = betterproto.int32_field(5, optional=True)
    show_headline: bool = betterproto.bool_field(6, optional=True)
    headline_aggregation: str = betterproto.string_field(7, optional=True)
    headline_client_state: str = betterproto.string_field(8, optional=True)


@dataclass(eq=False, repr=False)
class ChartVisualization(betterproto.Message):
    type: str = betterproto.string_field(1, optional=True)
    chart_columns: List["ChartVisualizationChartColumn"] = betterproto.message_field(2, optional=True)
    axis_configs: List["ChartVisualizationAxisConfig"] = betterproto.message_field(3, optional=True)
    locked: bool = betterproto.bool_field(4, optional=True)
    client_state: str = betterproto.string_field(5, optional=True)
    client_state_v2: str = betterproto.string_field(6, optional=True)

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.is_set("locked"):
            warnings.warn("ChartVisualization.locked is deprecated", DeprecationWarning)


@dataclass(eq=False, repr=False)
class ChartVisualizationChartColumn(betterproto.Message):
    column_id: str = betterproto.string_field(1, optional=True)
    conditional_formatting: "ConditionalFormattingProto" = betterproto.message_field(2, optional=True)
    show_data_labels: bool = betterproto.bool_field(3, optional=True)


@dataclass(eq=False, repr=False)
class ChartVisualizationAxisConfig(betterproto.Message):
    x: List[str] = betterproto.string_field(1, optional=True)
    y: List[str] = betterproto.string_field(2, optional=True)
    color: List[str] = betterproto.string_field(3, optional=True)
    size: str = betterproto.string_field(4, optional=True)
    hidden: List[str] = betterproto.string_field(5, optional=True)
    category: List[str] = betterproto.string_field(6, optional=True)
    sort: List[str] = betterproto.string_field(7, optional=True)


@dataclass(eq=False, repr=False)
class AnswerEDocProto(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    description: str = betterproto.string_field(2, optional=True)
    tables: List["Identity"] = betterproto.message_field(3, optional=True)
    joins: List["Join"] = betterproto.message_field(4, optional=True)
    table_paths: List["TablePath"] = betterproto.message_field(5, optional=True)
    formulas: List["Formula"] = betterproto.message_field(6, optional=True)
    search_query: str = betterproto.string_field(7, optional=True)
    answer_columns: List["AnswerEDocProtoAnswerColumn"] = betterproto.message_field(8, optional=True)
    table: "TableVisualization" = betterproto.message_field(9, optional=True)
    chart: "ChartVisualization" = betterproto.message_field(10, optional=True)
    display_mode: str = betterproto.string_field(11, optional=True)
    client_state: str = betterproto.string_field(12, optional=True)
    parameters: List["Parameter"] = betterproto.message_field(13, optional=True)
    parameter_values: Dict[str, str] = betterproto.map_field(14, betterproto.TYPE_STRING, betterproto.TYPE_STRING)

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.is_set("client_state"):
            warnings.warn("AnswerEDocProto.client_state is deprecated", DeprecationWarning)


@dataclass(eq=False, repr=False)
class AnswerEDocProtoAnswerColumn(betterproto.Message):
    id: str = betterproto.string_field(1, optional=True)
    name: str = betterproto.string_field(2, optional=True)
    custom_name: str = betterproto.string_field(3, optional=True)
    format: "FormatConfig" = betterproto.message_field(4, optional=True)


@dataclass(eq=False, repr=False)
class PinnedVisualization(betterproto.Message):
    id: str = betterproto.string_field(1, optional=True)
    answer: "AnswerEDocProto" = betterproto.message_field(2, optional=True)
    display_headline_column: str = betterproto.string_field(3, optional=True)
    viz_guid: str = betterproto.string_field(5, optional=True)


@dataclass(eq=False, repr=False)
class PinboardLayout(betterproto.Message):
    tabs: List["PinboardLayoutTab"] = betterproto.message_field(1, optional=True)
    tiles: List["PinboardLayoutTile"] = betterproto.message_field(2, optional=True)


@dataclass(eq=False, repr=False)
class PinboardLayoutTab(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    description: str = betterproto.string_field(2, optional=True)
    tiles: List["PinboardLayoutTile"] = betterproto.message_field(3, optional=True)


@dataclass(eq=False, repr=False)
class PinboardLayoutTile(betterproto.Message):
    visualization_id: str = betterproto.string_field(1, optional=True)
    size: str = betterproto.string_field(2, optional=True)
    x: int = betterproto.int32_field(3, optional=True)
    y: int = betterproto.int32_field(4, optional=True)
    height: int = betterproto.int32_field(5, optional=True)
    width: int = betterproto.int32_field(6, optional=True)

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.is_set("size"):
            warnings.warn("PinboardLayoutTile.size is deprecated", DeprecationWarning)


@dataclass(eq=False, repr=False)
class PinboardParameterOverrideEDoc(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    id: str = betterproto.string_field(2, optional=True)
    excluded_container_id: List[str] = betterproto.string_field(3, optional=True)
    override_value: str = betterproto.string_field(4, optional=True)
    secondary_parameter: List[str] = betterproto.string_field(5, optional=True)


@dataclass(eq=False, repr=False)
class PinboardEDocProto(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    description: str = betterproto.string_field(2, optional=True)
    tables: List["Identity"] = betterproto.message_field(3, optional=True)
    visualizations: List["PinnedVisualization"] = betterproto.message_field(4, optional=True)
    filters: List["Filter"] = betterproto.message_field(5, optional=True)
    layout: "PinboardLayout" = betterproto.message_field(6, optional=True)
    parameters: List["Parameter"] = betterproto.message_field(7, optional=True)
    parameter_overrides: Dict[str, "PinboardParameterOverrideEDoc"] = betterproto.map_field(
        8, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )


@dataclass(eq=False, repr=False)
class LogicalTableEDocProto(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    description: str = betterproto.string_field(2, optional=True)
    db: str = betterproto.string_field(3, optional=True)
    schema: str = betterproto.string_field(4, optional=True)
    db_table: str = betterproto.string_field(5, optional=True)
    connection: "Identity" = betterproto.message_field(6, optional=True)
    columns: List["LogicalTableEDocProtoLogicalColumnEDocProto"] = betterproto.message_field(7, optional=True)
    rls_rules: "LogicalTableEDocProtoRlsRule" = betterproto.message_field(8, optional=True)
    joins_with: List["RelationEDocProto"] = betterproto.message_field(9, optional=True)


@dataclass(eq=False, repr=False)
class LogicalTableEDocProtoRlsRule(betterproto.Message):
    tables: List["Identity"] = betterproto.message_field(1, optional=True)
    joins: List["Join"] = betterproto.message_field(2, optional=True)
    table_paths: List["TablePath"] = betterproto.message_field(3, optional=True)
    rules: List["LogicalTableEDocProtoRlsRuleRule"] = betterproto.message_field(4, optional=True)
    table: "Identity" = betterproto.message_field(5, optional=True)


@dataclass(eq=False, repr=False)
class LogicalTableEDocProtoRlsRuleRule(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    expr: str = betterproto.string_field(2, optional=True)


@dataclass(eq=False, repr=False)
class LogicalTableEDocProtoLogicalColumnEDocProto(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    description: str = betterproto.string_field(2, optional=True)
    db_column_name: str = betterproto.string_field(3, optional=True)
    properties: "ColumnProperties" = betterproto.message_field(4, optional=True)
    db_column_properties: "LogicalTableEDocProtoDbColumnProperties" = betterproto.message_field(5, optional=True)


@dataclass(eq=False, repr=False)
class LogicalTableEDocProtoDbColumnProperties(betterproto.Message):
    data_type: str = betterproto.string_field(1, optional=True)


@dataclass(eq=False, repr=False)
class SqlViewEDocProto(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    description: str = betterproto.string_field(2, optional=True)
    connection: "Identity" = betterproto.message_field(3, optional=True)
    sql_query: str = betterproto.string_field(4, optional=True)
    sql_view_columns: List["SqlViewEDocProtoSqlViewColumn"] = betterproto.message_field(5, optional=True)
    joins_with: List["RelationEDocProto"] = betterproto.message_field(6, optional=True)


@dataclass(eq=False, repr=False)
class SqlViewEDocProtoSqlViewColumn(betterproto.Message):
    name: str = betterproto.string_field(1, optional=True)
    description: str = betterproto.string_field(2, optional=True)
    sql_output_column: str = betterproto.string_field(3, optional=True)
    properties: "ColumnProperties" = betterproto.message_field(4, optional=True)
