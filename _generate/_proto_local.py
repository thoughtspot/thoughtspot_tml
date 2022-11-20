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
