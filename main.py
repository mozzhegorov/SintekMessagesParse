import xml.etree.ElementTree as tree
import csv
from io import StringIO

OIP_FILTER = [1, 2, *range(16, 21), 40, 44, 47, 51, 53, 56, 58, *range(350, 418)]
DP_FILTER = [*range(1, 51), *range(90, 418)]
DP_ADDITION = {
    "on": {
        0: [66, ],
        3: [66, ],
        2: [61, ],
        1: [60, ],
        6: [66, ],
        9: [66, ],
        5: [66, ],
        4: [66, ],
    },
    "off": {
        0: [88, ],
        3: [88, ],
        2: [86, ],
        1: [87, ],
        6: [88, ],
        9: [88, ],
        5: [88, ],
        4: [88, ],
    },
}
COLORS = {
    0: "Белый",
    1: "Красный",
    2: "Желтый",
    3: "Цвет3",
    9: "Зеленый",
    4: "цвет4",
    700: "Красный",
    701: "Желтый",
}
STATION = "tyumen"


def get_table_string(signal, external):
    severity = int(external.attrib["Severity"])
    color = COLORS[severity]
    sound = external.attrib['Sound'] if external.attrib['Sound'] else ''
    return [
        f"{signal}{external.attrib['Message']}",
        color,
        sound,
        severity,
    ]


def recurency_find(data: tree.Element, signal_filter):
    result = []
    for item in data:
        if "Type" in item.attrib and item.attrib["Type"] == "Folder":
            result.extend(recurency_find(item.find("Items"), signal_filter))
        properties = item.find("Properties")
        if properties:
            for prop in properties:
                if hasattr(prop, "attrib") and \
                        "Value" in prop.attrib and \
                        prop.attrib["Value"] == signal_filter and \
                        properties[0].attrib["Value"] != signal_filter and \
                        "Резерв" not in properties[0].attrib["Value"] and \
                        "РЕЗЕРВ" not in properties[0].attrib["Value"]:
                    result.append(properties[0].attrib["Value"])
    return result


def xpath_find(data: tree.Element, signal_filter):
    result = []
    properties_group = data.findall(".//Properties")
    for prop in properties_group:
        prop_type = prop.find(".//*[@Id='999000']")
        prop_name = prop.find(".//*[@Id='101']")
        if isinstance(prop_type, tree.Element) and \
                isinstance(prop_name, tree.Element) and \
                "Резерв" not in prop_name.attrib["Value"] and \
                "РЕЗЕРВ" not in prop_name.attrib["Value"] and \
                prop_type.attrib["Value"] == signal_filter:
            result.append(prop_name.attrib["Value"])
    return result


def oip_generate(signals, external, *args):
    result = []
    for signal in signals:
        for addition in external:
            if (int(addition.attrib['Value']) in OIP_FILTER or len(external) > 40) \
                    and int(addition.attrib['Enabled']):
                result.append(get_table_string(signal, addition))
    return result


def universal_generate(signals, external, *args):
    result = []
    for signal in signals:
        for addition in external:
            if int(addition.attrib['Enabled']):
                result.append(get_table_string(signal, addition))
    return result


def dp_generate(signals, external, *args):
    result = []
    dp_extra_filter = {}
    for dp in args[0]:
        name = dp.find("comment").text.capitalize()
        dp_extra_filter[name] = int(dp.find(".//*[@name='nTYPE_ALM']").find("value").text)

    for signal in signals:
        for addition in external:
            cap_signal = signal.capitalize()
            on, off = 0, 0
            if cap_signal in dp_extra_filter:
                off, on = divmod(dp_extra_filter[cap_signal], 10)

            if (int(addition.attrib['Value']) in DP_FILTER or
                int(addition.attrib['Value']) in DP_ADDITION["on"][on] or
                int(addition.attrib['Value']) in DP_ADDITION["off"][off]) and \
                    int(addition.attrib['Enabled']):
                result.append(get_table_string(signal, addition))
    return result


types_methods = {
    "Измеряемый параметр (6 уставок)": oip_generate,
    "Дискретный параметр": dp_generate,
}


def csv_write(msgs: list):
    with open(f'{STATION}.csv', 'w', newline='') as csvfile:
        msgwriter = csv.writer(
            csvfile,
            delimiter=';',
            quotechar=';',
            quoting=csv.QUOTE_MINIMAL,
        )
        msgwriter.writerows(msgs)


def newcsv(data, fieldnames=""):
    """
    Create a new csv file that represents generated data.
    """
    new_csvfile = StringIO()
    wr = csv.writer(
        new_csvfile,
        quoting=csv.QUOTE_NONE,
        delimiter=';',
        lineterminator='\r\n',
        quotechar=";",
    )

    wr.writerow(("Сообщение", "Цвет", "Звук", "Severity", ))
    for item in data:
        wr.writerow(item)

    return new_csvfile


def generate_messages_file(alpha_config_raw, external_objects_raw, dp_in_prg_raw):
    alpha_config = tree.fromstring(alpha_config_raw) \
        .find("Signals") \
        .find("Items")
    external_objects = tree.fromstring(external_objects_raw) \
        .find("Types")
    dp_in_prg = tree.fromstring(dp_in_prg_raw) \
        .find("dataBlock") \
        .find("variables") \
        .findall("instanceElementDesc")

    all_messages = []
    for signal_type in external_objects:
        type_name = signal_type.attrib["Name"]
        conditions = signal_type.find("EventConditions").find("EventCondition")
        signals_of_type = xpath_find(alpha_config, type_name)
        messages = None
        if conditions and type_name in types_methods:
            messages = types_methods[type_name](signals_of_type, conditions, dp_in_prg)
        elif conditions:
            messages = universal_generate(signals_of_type, conditions)
        if messages:
            all_messages.extend(messages)
    return newcsv(all_messages)


if __name__ == "__main__":
    pass
