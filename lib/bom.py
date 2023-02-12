import json
import cadquery as cq
import cadquery.cqgi as cqgi


class BomPart:
    def __init__(self, name, path, config, data):
        self.name = name
        self.path = path
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
        self.data = data
        self.count = 1

    def print(self):
        print(self.name, ": ", self.count)


class Bom:
    def __init__(self):
        self.parts = {}

    def get_part(self, path):
        part = json.loads(open(path + "/part.json").read())
        result = None

        # Create the line item if it's not there yet
        if not path in self.parts:
            self.parts[path] = BomPart(part["name"], path, part, result)
        else:
            self.parts[path].count = self.parts[path].count + 1

        # Load the data if it's not there yet
        if self.parts[path].data is None:
            if part["type"] == "step":
                result = cq.importers.importStep(path + "/part.step")
            self.parts[path].data = result
        else:
            result = self.parts[path].data

        return result, part["name"]

    def add_part(self, assembly, path):
        part, name = self.get_part(path)
        assembly.add(part, name=name)
        return part

    def get_assembly(self, path):
        model = cqgi.parse(open(path).read())
        build_result = model.build()
        result = build_result.results[0]
        shape = result.shape.toCompound()
        bom_base = result.options["bom"]

        self.extend(bom_base)
        return shape, result.options["name"]

    def add_assembly(self, assembly, path, name=None):
        shape, shape_name = self.get_assembly(path)
        if name is None:
            name = shape_name
        assembly.add(shape, name=name)
        return shape

    def extend(self, other):
        for path in other.parts:
            part = other.parts[path]
            if path in self.parts:
                self.parts[path].count += part.count
            else:
                self.parts[path] = part

    def print(self):
        for path in self.parts:
            part = self.parts[path]
            part.print()

    def write(self, path):
        bom_lines = [
            "# Don1\n",
            "## Bill of Materials\n",
            "| Part | Count | Vendor | SKU | Preview |\n",
            "| -- | -- | -- | -- | -- |\n",
        ]
        for part_path in self.parts:
            part = self.parts[part_path]
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
                + str(part.count)
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
        bom_file = open(path, "w+")
        bom_file.writelines(bom_lines)
        bom_file.close()
