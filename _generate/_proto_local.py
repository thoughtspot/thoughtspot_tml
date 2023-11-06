"""
@boonhapus, 2022/11/18

Not all protos live as part of the base Edoc proto. If you truly need to understand this
package to build a new version, please consult one of the maintainers of this library.
"""

# common/common.proto
# package common;
PROTO_COMMON = r"""
message KeyValueStr {
    optional string key = 1;
    optional string value = 2;
}

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
"""

# protos/number_format.proto
# package blink.numberFormatConfig;
PROTO_NUMBER_FORMAT_CONFIG = r"""
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

# public/metadata.proto
# package atlas;
PROTO_ATLAS_ACTION_CONTEXT = r"""
message ActionContext {
  enum E {
    NONE = 0;
    PRIMARY = 1;
    MENU = 2;
    CONTEXT_MENU = 3;
  }
}

message ActionObjectApplicationType {
  enum E {
    NONE = 0;
    SLACK = 1;
    SALESFORCE = 2;
    GOOGLE_SHEET = 3;
  }
}
"""


# /monitor/monitor_rule.proto
# package a3.metric_monitor;
PROTO_MONITOR_SUPPLEMENTAL = r"""
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
"""
