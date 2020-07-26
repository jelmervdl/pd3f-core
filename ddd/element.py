from tqdm import tqdm

from .dehyphen import is_split_paragraph


class Document:
    def __init__(self, data, order):
        self.data = data or []
        self.order = order or []
        self.merged_elements = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def get_element(self, elem_id):
        if elem_id in self.merged_elements:
            elem_id = self.merged_elements[elem_id]
        return list(filter(lambda x: x.id == elem_id, self))[0]

    def get_first_of_type_on_page(self, find_types, page_num):
        for ele_id in self.order[page_num]:
            ele = self.get_element(ele_id)
            if ele.type in find_types:
                return ele
        return None

    def get_last_of_type_on_page(self, find_types, page_num):
        for ele_id in reversed(self.order[page_num]):
            ele = self.get_element(ele_id)
            if ele.type in find_types:
                return ele
        return None

    def reverse_page_break(self, debug=False):
        """join paragraphs that were split between pages

        gets complicated when footnotes are not re-ordered
        """
        for idx, page in tqdm(
            enumerate(self.order[:-1]), desc="trying to reverse page breaks"
        ):
            last_element = self.get_last_of_type_on_page(("body", "heading"), idx)
            next_element = self.get_first_of_type_on_page(("body", "heading"), idx + 1)

            if last_element is None or next_element is None:
                continue

            if last_element.type == "heading" or next_element.type == "heading":
                continue

            # It cannot contain newlines
            if last_element.num_newlines > 0:
                if debug:
                    print(
                        f"the last element has {last_element.num_newlines} newlines. Do not try to join with the next one."
                    )
                continue

            fixed = is_split_paragraph(last_element, next_element)
            if fixed is None:
                continue

            if debug:
                print("joining the following paragraphs")
                print(last_element, next_element)
            # set new paragraph
            self[self.data.index(last_element)] = fixed
            self.data.remove(next_element)
            self.merged_elements[next_element.id] = last_element.id

    def reorder_footnotes(self):
        new_data = []
        all_footsnotes = []
        for element in self:
            if element.type == "footnotes":
                all_footsnotes.append(element)
            else:
                new_data.append(element)

        self.data = new_data + all_footsnotes

    def markdown(self):
        return self.text(markdown=True)

    def text(self, markdown=False):
        txt = ""
        for element in self:
            if markdown and element.type == "heading":
                # prepend dashes
                txt += "#" * element.level + " "
            txt += str(element)
        return txt


class Element:
    def __init__(self, element_type, lines, element_id, num_newlines=0, level=None):
        assert element_type in ("body", "heading", "footnotes")
        self.type = element_type
        self.lines = lines
        self.id = element_id
        self.level = level
        self.num_newlines = num_newlines

    def __getitem__(self, key):
        return self.lines[key]

    def __str__(self):
        # FIXME
        if self.type == "footnotes":
            return "".join([" ".join(line) for line in self.lines]) + "\n"
        return "".join([" ".join(line) for line in self.lines]) + "\n\n"

    def __add__(self, other_element):
        assert self.type == other_element.type
        self.lines += other_element.lines
        return self