# Worksheet Remapping (Namespace)

Worksheets are __ThoughtSpot's__ logical or semantic layer; a collection of related tables with optional business logic added in the form of Formulas.

In this example, we leverage the pattern outlined in [Development and Deployment][guide-deploy] which helps in maintaining changes across development environments.

The core idea revolves around having content names that are structured for disambiguation. All objects in __ThoughtSpot__ have a globally unique id or GUID, but historically, default parameters in the APIs do not include underlying objects' guid in the output. TML offers a way to disambiguate objects which share a core type and have the same name through the use of the `fqn` key on each object.

This concept is called [namespacing][wiki-namespace].

| __TS Object__  | <b>DEV</b>elopment | __TEST__            | <b>PROD</b>uction |
| :---           | :---               | :---                | :---              |
| `Connection`   | Analytics (Dev)    | Analytics (Test)    | Analytics         |
| `System Table` | DEV_FCT_SALES      | TEST_FCT_SALES      | FCT_SALES         |
| `System Table` | DEV_DIM_CUSTOMERS  | TEST_DIM_CUSTOMERS  | DIM_CUSTOMERS     |
| `System Table` | DEV_DIM_PRODUCTS   | TEST_DIM_PRODUCTS   | DIM_PRODUCTS      |
| `System Table` | DEV_DIM_STORES     | TEST_DIM_STORES     | DIM_STORES        |
| `Worksheet`    | DEV_Retail_Sales   | TEST_Retail_Sales   | Retail Sales      |

Assuming your environment is set up like the above table, we can leverage the `worksheet_remapping` program to replace one prefix with another.

The code block that performs this activity is below.

```python
    # Build a regular expression which matches the source prefix at the beginning of a string
    RE_SRC_NAMESPACE = re.compile(fr"^{args.source_prefix}.*")

    # Replace instances of DEV_ with TEST_
    tml.worksheet.name = RE_SRC_NAMESPACE.sub(args.target_prefix, tml.worksheet.name)

    for table in tml.worksheet.tables:
        table.name = RE_SRC_NAMESPACE.sub(args.target_prefix, table.name)
```

---

```shell
>>> python worksheet_remapping.py -h

usage: [-h] [-s SRC] [-d DST] worksheet_tml

positional arguments:
  worksheet_tml         a worksheet.tml to remap

options:
  -h, --help                show this help message and exit
  -s SRC, --src-prefix SRC  (default: DEV_)
  -d DST, --dst-prefix DST  (default: TEST_)
```

[guide-deploy]: https://developers.thoughtspot.com/docs/?pageid=development-and-deployment#_dev_test_prod
[wiki-namespace]: https://en.wikipedia.org/wiki/Namespace
