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

// This message captures simple and advance grouping in cohorts.
// sage.DateFilterProto is Modified from the original, to adjust for the name space issue
// 

message FilterCondition {
  enum FilterValueType {
    STRING=1;
    DATE_FILTER=2;
  }
  optional string column_id = 1;
  optional ComparisonOperator.E operator = 2;
  repeated string value = 3;
  optional string column_name = 4;
  optional FilterValueType filter_value_type = 5 [default = STRING];

  repeated SageDateFilterProto date_filter_values = 6;
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

message PassThruFilter {
  optional bool accept_all = 1;
  repeated string include_column_ids = 2;
  repeated string exclude_column_ids = 3;
}

message CohortConfig {
  enum Version {
    V1 = 1;
    V1DOT1 = 2;
  }
  optional string name = 1;
  optional string description = 2;

  optional string null_output_value = 3;

  optional bool combine_non_group_values = 4 [default = true];
  optional CohortType.E cohort_type = 5;
  optional CohortGroupingType.E cohort_grouping_type = 10;

  optional string anchor_column_id = 6;

  optional string return_column_id = 7;
  repeated CohortGroup groups = 8;
  optional CohortBin bins = 9;
  optional string cohort_answer_guid = 11;
  optional bool is_editable = 12 [default = false];

  optional string cohort_guid = 13 [deprecated = true];

  optional bool hide_excluded_query_values = 14 [default = true];

  optional string group_excluded_query_values = 15;
  optional Version version = 16;
  optional PassThruFilter pass_thru_filter = 17;
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


// bryanthowell-ts 2025-10-09
// from sage/public/date_filter.proto

message SageDateFilterProto {
  enum DatePeriod {
    DAY = 0;
    WEEK = 1;
    MONTH = 2;
    QUARTER = 3;
    YEAR = 4;
    HOUR = 5;
    MINUTE = 6;
    SECOND = 7;
    NUM_DATE_PERIODS = 8;
  }

  enum Quarter {
    Q1 = 0;
    Q2 = 1;
    Q3 = 2;
    Q4 = 3;
    NUM_QUARTERS = 4;
  }

  enum Month {
    JANUARY = 0;
    FEBRUARY = 1;
    MARCH = 2;
    APRIL = 3;
    MAY = 4;
    JUNE = 5;
    JULY = 6;
    AUGUST = 7;
    SEPTEMBER = 8;
    OCTOBER = 9;
    NOVEMBER = 10;
    DECEMBER = 11;
    NUM_MONTHS = 12;
  }

  enum WeekDay {
    MONDAY = 0;
    TUESDAY = 1;
    WEDNESDAY = 2;
    THURSDAY = 3;
    FRIDAY = 4;
    SATURDAY = 5;
    SUNDAY = 6;
    NUM_WEEK_DAYS = 7;
  }

  enum DateFilterType {
    YESTERDAY = 0;
    TODAY = 1;
    TOMORROW = 18;
    LAST_PERIOD = 2;       // e.g., Last Week
    LAST_N_PERIOD = 3;     // e.g., Last 2 week
    PERIOD_TO_DATE = 4;    // e.g., month to date
    YEAR_ONLY = 5;         // e.g., 2014
    QUARTER_YEAR = 6;      // e.g., Q1 2014
    QUARTER_ONLY = 20;     // e.g., Q1
    MONTH_ONLY = 7;        // e.g., January
    WEEKDAY_ONLY = 8;      // e.g., Monday
    MONTH_YEAR = 9;        // e.g., January 2014
    N_PERIOD_AGO = 10;     // e.g., 2 day ago
    THIS_PERIOD = 13;      // e.g. This Week
    NEXT_PERIOD = 14;      // e.g. Next Week
    NEXT_N_PERIOD = 17;    // e.g. Next 7 week
    EXACT_DATE = 11;       // e.g., 12/31/2014
    EXACT_TIME = 19;       // e.g., 10:05
    EXACT_DATE_TIME = 12;  // e.g., 12/31/2014 23:59:59
    NOW = 15;  // same as EXACT_DATE_TIME but interpreted when query executes
    EXACT_DATE_RANGE = 16;
    PERIOD_ONLY = 21;      // Used to specify a date bucket filter.
                           // e.g. "week of year = 50"
    // Keep it as highest value.
    NUM_DATE_FILTERS = 22;
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
