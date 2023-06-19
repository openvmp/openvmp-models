import json
import cadquery as cq
import cadquery.cqgi as cqgi
import math


class BomPart:
    def __init__(self, name, path, config, data):
        self.name = name
        self.path = path
        self.config = config
        self.data = data

        self.desc = None
        if "desc" in config:
            self.desc = config["desc"]
        self.vendor = None
        if "vendor" in config:
            self.vendor = config["vendor"]
        self.sku = None
        if "sku" in config:
            self.sku = config["sku"]
        self.url = None
        if "url" in config:
            self.url = config["url"]
        if "count_per_sku" in config:
            self.count_per_sku = config["count_per_sku"]
        else:
            self.count_per_sku = 1
        self.count = 1

    def clone(self):
        cloned = BomPart(self.name, self.path, self.config, self.data)
        cloned.count = self.count
        return cloned

    def print(self):
        print(self.name, ": ", self.count)


class Bom:
    # parts is a static member that contains all parts in the model
    parts = {}

    def __init__(self):
        # self.self_parts contains all parts in the assembly for ease of cloning
        self.self_parts = {}

        # sel.assemblies contains all assemblies loaded so far
        self.assemblies = {}

    def get_part(self, path):
        part = json.loads(open(path + "/part.json").read())
        result = None

        # Create the line item if it's not there yet
        if not path in Bom.parts:
            Bom.parts[path] = BomPart(part["name"], path, part, result)
        else:
            Bom.parts[path].count = Bom.parts[path].count + 1

        if not path in self.self_parts:
            self.self_parts[path] = BomPart(part["name"], path, part, None)
        else:
            self.self_parts[path].count = self.self_parts[path].count + 1

        # Load the data if it's not there yet
        if Bom.parts[path].data is None:
            if part["type"] == "step":
                result = cq.importers.importStep(path + "/part.step")
            Bom.parts[path].data = result
        else:
            result = Bom.parts[path].data

        return result, part["name"]

    def add_part(self, assembly, path):
        part, name = self.get_part(path)
        assembly.add(part, name=name)
        return part

    def get_assembly(self, path):
        shape = None
        name = None
        # Load the data if it's not processed yet
        if not path in self.assemblies:
            file = open(path)
            model = cqgi.parse(file.read())
            file.close()
            build_result = model.build()
            result = build_result.results[0]

            shape = result.shape.toCompound()
            name = result.options["name"]
            parts = result.options["parts"]
            self.assemblies[path] = (shape, name, parts)
        else:
            (shape, name, parts) = self.assemblies[path]
            self.extend(parts)

        return shape, name

    def add_assembly(self, assembly, path, name=None):
        shape, shape_name = self.get_assembly(path)
        if name is None:
            name = shape_name
        assembly.add(shape, name=name)
        return shape

    def extend(self, parts):
        for path in parts:
            part = parts[path]
            if path in Bom.parts:
                Bom.parts[path].count += part.count
            else:
                Bom.parts[path] = part.clone()

    def print(self):
        print("BoM:")
        for path in Bom.parts:
            part = Bom.parts[path]
            part.print()

    def write(self, name, path):
        bom_lines = [
            "# " + name + "\n",
            "## Bill of Materials\n",
            "| Part | Count* | Vendor | SKU | Preview |\n",
            "| -- | -- | -- | -- | -- |\n",
        ]
        for part_path in Bom.parts:
            part = Bom.parts[part_path]
            name = part.name
            vendor = ""
            sku = ""
            if not part.desc is None:
                name = part.desc
            if not part.vendor is None:
                vendor = part.vendor
            if not part.sku is None:
                sku = part.sku
            if not part.url is None:
                if sku == "":
                    vendor = "[" + vendor + "](" + part.url + ")"
                else:
                    sku = "[" + sku + "](" + part.url + ")"
            bom_lines.append(
                "| ["
                + name
                + "](../../../"
                + part.path
                + "/README.md) | "
                + str(math.ceil(part.count / part.count_per_sku))
                + " |"
                + vendor
                + " |"
                + sku
                + " |"
                + " !["
                + name
                + "](../../"
                + part_path
                + ".svg)"
                + " |\n"
            )
        bom_lines.append(
            """
(\\*) The `Count` field is the number of SKUs to be ordered.
It already takes into account the number of items per SKU.
            """
        )
        bom_file = open(path, "w+")
        bom_file.writelines(bom_lines)
        bom_file.close()
