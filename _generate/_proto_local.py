# noqa: I002
"""
@boonhapus, 2022/11/18

Not all protos live as part of the base Edoc proto. If you truly need to understand this
package to build a new version, please consult one of the maintainers of this library.
"""

# DEV NOTE @
# LAST UPDATE: 2024/11/10 , v10.3.0.cl
#  PROTO PATH: datamanager/public/query_triggers.proto
#  PROTO NAME: package datamanager;
#
PROTO_DATAMANAGER_QUERY_TRIGGERS = r"""

// ====================================================
// QueryTrigger.E
// ====================================================

message QueryTrigger {
  enum E {
    UNKNOWN = 1;
    ANSWER_EDIT = 2;
    ANSWER_VIEW = 3;
    LIVEBOARD_EDIT = 4;
    LIVEBOARD_VIEW = 5;
    UNDERLYING_DATA = 6;
    DOWNLOAD = 7;
    EXPLORE = 8;
    DRILL_DOWN = 9;
    DATA_WORKSPACE_QUERY = 10;
    SEARCH_DATA = 11;
    SPOTIQ_AUTO_ANALYZE = 12;
    KPI_MONITOR = 13;
    GET_FILTER_VALUES = 14;
    TS_SYNC = 15;
    MOBILE = 16;
    APIS = 17;
    CDW_CONNECTION = 18;
    DATA_WORKSPACE_SAMPLE = 19;
    SQL_EDITOR = 20;
    DBT = 21;
    SAGE_INDEXING = 22;
    SPOT_APPS = 23;
    ROW_COUNT_STATS = 24;
    SAGE_SAMPLING = 25;
    SCHEDULED_PINBOARDS = 26;
    REPORTBOOK = 27;
    CAFFEINE = 28;
    CORTEX = 29;
    SEED_QUESTIONS = 30;
    CUSTOM_CALENDAR = 31;
  }
}
"""


# DEV NOTE @
# LAST UPDATE: 2025/01/06 , v10.5.0.cl
#  PROTO PATH: callosum/public/metadata/answer_spec.proto
#  PROTO NAME: package entitylib;
#
PROTO_CALLOSUM_ANSWER_SPEC = r"""

// ====================================================
// ChartVizProto.ChartSpecificColumn.Type
// ====================================================

message ChartVizProto {
  message ChartSpecificColumn {
    enum Type {
      UNDEFINED = 0;
      MEASURE_NAMES = 1;
      MEASURE_VALUES = 2;
    }
    optional Type type = 3;
  }
}


// ====================================================
// Chip.ChipType
// ====================================================

message Chip {
  enum ChipType {
    FILTER = 0;
    PARAMETER = 1;
  }

  required string object_id = 1;
  required ChipType type = 2;
}
"""

# DEV NOTE @boonhapus
# LAST UPDATE: 2024/11/10 , v10.3.0.cl
#  PROTO PATH: callosum/public/cohort.proto
#  PROTO NAME: package callosum;
#
PROTO_CALLOSUM_COHORT = r"""

// ====================================================
// CohortType.E
// ====================================================

message CohortType {
  enum E {
    SIMPLE = 1;
    ADVANCED = 2;
    GROUP_BASED = 3 [deprecated = true];
    BIN_BASED = 4 [deprecated = true];
    COLUMN_BASED = 5 [deprecated = true];
  }
}

// ====================================================
// CohortGroupingType.E
// ====================================================

message CohortGroupingType {
  enum E {
    GROUP_BASED = 1;
    BIN_BASED = 2;
    COLUMN_BASED = 3;
  }
}

// ====================================================
// CohortGroup
// ====================================================

message ConditionCombineType {
  enum E {
    ALL = 1;
    ANY = 2;
  }
}

message ComparisonOperator {
  enum E {
    EQ = 1;
    NE = 2;
    LT = 3;
    LE = 4;
    GT = 5;
    GE = 6;
    BW = 7;
    CONTAINS = 8;
    NOT_CONTAINS = 9;
    BEGINS_WITH = 10;
    ENDS_WITH = 11;
  }
}

message FilterCondition {
  optional string column_id = 1;
  optional ComparisonOperator.E operator = 2;
  repeated string value = 3;
  optional string column_name = 4;
}

message CohortGroup {
  optional string name = 1;
  repeated FilterCondition conditions = 2;
  optional ConditionCombineType.E combine_type = 3;
}

// ====================================================
// CohortBin
// ====================================================

message CohortBin {
  optional double minimum_value = 1;
  optional double maximum_value = 2;
  optional double bin_size = 3;
}
"""


# DEV NOTE @boonhapus
# LAST UPDATE: 2024/11/10 , v10.3.0.cl
#  PROTO PATH: sage/public/common.proto
#  PROTO NAME: package sage;
#
PROTO_SAGE = r"""

// ====================================================
// TimeBucket.E
// ====================================================

message TimeBucket {
  enum E {
    NO_BUCKET = 0;
    DAILY = 1;
    WEEKLY = 2;
    MONTHLY = 3;
    QUARTERLY = 4;
    YEARLY = 5;
    HOURLY = 6;
    AUTO = 8;

    HOUR_OF_DAY = 9;
    DAY_OF_WEEK = 7;
    DAY_OF_MONTH = 10;
    DAY_OF_QUARTER = 11;
    DAY_OF_YEAR = 12;
    WEEK_OF_MONTH = 13;
    WEEK_OF_QUARTER = 14;
    WEEK_OF_YEAR = 15;
    MONTH_OF_QUARTER = 16;
    MONTH_OF_YEAR = 17;
    QUARTER_OF_YEAR = 18;
  }
}
"""


# DEV NOTE @boonhapus
# LAST UPDATE: 2024/11/10 , v10.3.0.cl
#  PROTO PATH: protos/number_format.proto
#  PROTO NAME: package blink.numberFormatConfig;
#
PROTO_NUMBER_FORMAT_CONFIG = r"""

// ====================================================
// FormatConfig
// ====================================================

message FormatConfig {
    enum CategoryType {
        NUMBER = 1;
        PERCENTAGE = 2;
        CURRENCY = 3;
        CUSTOM = 4;
    }
    enum Unit {
        NONE = 1;
        THOUSANDS = 2;
        MILLION = 3;
        BILLION = 4;
        TRILLION = 5;
        AUTO = 6;
    }
    enum NegativeValueFormat {
        PREFIX_DASH = 1;
        SUFFIX_DASH = 2;
        BRACES_NODASH = 3;
    }
    message NumberFormatConfig {
       optional Unit unit = 1 [default = AUTO];
       optional double decimals = 2 [default = 2];
       optional NegativeValueFormat negativeValueFormat = 3 [default = PREFIX_DASH];
       optional bool toSeparateThousands = 4 [default = true];
       optional bool removeTrailingZeroes = 5 [default = false];
    }
    message PercentageFormatConfig {
       optional double decimals = 1 [default = 2];
       optional bool removeTrailingZeroes = 2 [default = false];
    }
    message CurrencyFormatConfig {
       optional string locale = 1;
       optional Unit unit = 2 [default = MILLION];
       optional double decimals = 3 [default = 2];
       optional bool toSeparateThousands = 5 [default = true];
       optional bool removeTrailingZeroes = 6 [default = false];
    }
    message CustomFormatConfig {
        optional string format = 1;
    }
    optional CategoryType category = 1;
    oneof formatConfigDetails {
        NumberFormatConfig numberFormatConfig = 2;
        PercentageFormatConfig percentageFormatConfig = 3;
        CurrencyFormatConfig currencyFormatConfig = 4;
        CustomFormatConfig customFormatConfig = 5;
    }
    optional bool isCategoryEditable = 6 [default = true];
}
"""


# DEV NOTE @boonhapus
# LAST UPDATE: 2024/11/10 , v10.3.0.cl
#  PROTO PATH: common/common.proto
#  PROTO NAME: package common;
#
PROTO_COMMON = r"""

// ====================================================
// GeometryTypeEnum
// ====================================================

message GeometryTypeEnumProto {
  enum E {
    POINT = 0;
    LINE_STRING = 1;
    LINEAR_RING = 2;
    POLYGON = 3;
    MULTI_POINT = 4;
    MULTI_LINE_STRING = 5;
    MULTI_POLYGON = 6;
    GEOMETRY_COLLECTION = 7;
    CIRCLE = 8;
  }
}

// ====================================================
// KeyValueStr
// ====================================================

message KeyValueStr {
  optional string key = 1;
  optional string value = 2;
}
"""


# DEV NOTE @boonhapus
# LAST UPDATE: 2024/11/10 , v10.3.0.cl
#  PROTO PATH: atlas/public/metadata.proto
#  PROTO NAME: package atlas;
#
PROTO_ATLAS = r"""

// ====================================================
// QueryConstraints
// ====================================================

message QueryConstraints {
  message Constraint {
    message DateRangeCondition {
      enum Bucket {
        DAY = 0;
        WEEK = 1;
        MONTH = 2;
        QUARTER = 3;
        YEAR = 4;
      }
      optional string column = 1;
      optional int32 duration = 2;
      optional Bucket bucket = 3 [default = MONTH];
    }
    message Condition {
      optional DateRangeCondition date_range_condition = 1;
    }
    optional string table = 1;
    repeated Condition condition = 2;
    optional bool active = 3 [default = true];
  }
  repeated Constraint constraint = 1;
}

// ====================================================
// ChartViz.Config.CustomChartConfig
// ====================================================

message ChartViz {
  message Config {
    message CustomChartDimension {
      optional string key = 1;
      repeated string columns = 2;
    }

    message CustomChartConfig {
      optional string key = 1;
      repeated CustomChartDimension dimensions = 2;
    }
  }
}

// ====================================================
// ActionObjectApplicationType.E
// ====================================================

message ActionObjectApplicationType {
  enum E {
    NONE = 0;
    SLACK = 1;
    SALESFORCE = 2;
    GOOGLE_SHEET = 3;
  }
}

// ====================================================
// ActionContext.E
// ====================================================

message ActionContext {
  enum E {
    NONE = 0;
    PRIMARY = 1;
    MENU = 2;
    CONTEXT_MENU = 3;
  }
}
"""


# DEV NOTE @boonhapus
# LAST UPDATE: 2025/01/06 , v10.5.0.cl
#  PROTO PATH: a3/monitor/public/monitor_rule.proto
#  PROTO NAME: package a3.metric_monitor;
#
PROTO_KPI_MONITOR = r"""

// ====================================================
// FrequencySpec
// ====================================================

message FrequencySpec {
  enum FrequencyGranularity {
    EVERY_MINUTE = 0;
    HOURLY = 1;
    DAILY = 2;
    WEEKLY = 3;
    MONTHLY = 4;
  }

  message CronFrequencySpec {
      optional string second = 1;
      optional string minute = 2;
      optional string hour = 3;
      optional string day_of_month = 4;
      optional string month = 5;
      optional string day_of_week = 6;
  }
  optional CronFrequencySpec cron = 1;
  optional string time_zone = 2;
  optional int64 start_time = 3;
  optional int64 end_time = 4;
  optional FrequencyGranularity frequency_granularity = 5;
}

// ====================================================
// ConditionInfo
// ====================================================

enum Comparator {
  COMPARATOR_UNSPECIFIED = 0;
  COMPARATOR_LT = 1;
  COMPARATOR_GT = 2;
  COMPARATOR_LEQ = 3;
  COMPARATOR_GEQ = 4;
  COMPARATOR_EQ = 5;
  COMPARATOR_NEQ = 6;
}

enum PercentageChangeComparator {
  PERCENTAGE_CHANGE_COMPARATOR_UNSPECIFIED = 0;
  PERCENTAGE_CHANGE_COMPARATOR_INCREASES_BY = 1;
  PERCENTAGE_CHANGE_COMPARATOR_DECREASES_BY = 2;
  PERCENTAGE_CHANGE_COMPARATOR_CHANGES_BY = 3;
}

message ConstantValue {
  optional double value = 1;
}

message SimpleConditionInfo {
  optional Comparator comparator = 1;
  optional ConstantValue threshold = 2;
}

message PercentageChangeConditionInfo {
  optional PercentageChangeComparator comparator = 1;
  optional ConstantValue threshold = 2;
}

message ConditionInfo {
  oneof condition_info {
    SimpleConditionInfo simple_condition = 1;
    PercentageChangeConditionInfo percentage_change_condition = 2;
  }
}

// ====================================================
// MetricId
// ====================================================

message MetricId {
  message PinboardVizId {
    optional string pinboard_id = 1;
    optional string viz_id = 2;
  }
  oneof id {
    PinboardVizId pinboard_viz_id = 1;
    string answer_id = 2;
  }
  optional string personalised_view_id = 3;
}

// ====================================================
// AlertType
// ====================================================

enum AlertType {
  Scheduled = 0;
  Threshold = 1;
  Anomaly = 2;
}

// ====================================================
// AttributeInfo
// ====================================================

message AttributeInfo {
  optional string id = 1;
  repeated string values = 2;
  optional string answer_id = 3;
}
"""
