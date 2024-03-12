import pandas as pd


class DynamicFieldCSVReader:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = pd.read_csv(csv_path)
        self.dynamic_fields = {
            "DAS": {"count": 0, "length": 8, "total_length": 0, "count_position": (174, 176)},
            "CSARR": {"count": 0, "length": 35, "total_length": 0, "count_position": (176, 179)},
            "CCAM": {"count": 0, "length": 23, "total_length": 0, "count_position": (179, 181)}
        }
        self.dynamic_start_position = 187
        self.format_info = self._prepare_format_info()

    def _prepare_format_info(self):
        format_info = {}

        for _, row in self.df.iterrows():
            var_name, start, end = row['Libellé des variables'], row['Position début'], row['Position fin']
            if any(keyword in var_name for keyword in self.dynamic_fields.keys()):
                continue

            try:
                start = int(start)
            except ValueError:
                start = None
            try:
                end = int(end)
            except ValueError:
                end = None
            format_info[var_name] = (start, end)

        return format_info

    def _update_dynamic_counts(self, text_line):
        for field in self.dynamic_fields.keys():
            p1, p2 = self.dynamic_fields[field]['count_position']
            count = int(text_line[p1:p2].strip())
            self.dynamic_fields[field]['count'] = count
            self.dynamic_fields[field]['total_length'] = count * self.dynamic_fields[field]['length']


    def generate_dynamic_fields_positions(self):
        sum_length = 0
        for i in range(self.dynamic_fields['DAS']['count']):
            var_nam = f"DAS-{i}"
            sum_length = self.dynamic_start_position + (i * self.dynamic_fields['DAS']['length'])
            self.format_info[var_nam] = (sum_length, sum_length + self.dynamic_fields['DAS']['length'])
            sum_length += self.dynamic_fields['DAS']['length']

        for i in range(self.dynamic_fields['CSARR']['count']):
            var_nam = f"CSARR-{i}"
            self.format_info[f'{var_nam} - Code principal'] = (sum_length, sum_length + 7)
            sum_length += 7
            self.format_info[f'{var_nam} – Code supplémentaire (appareillage)'] = (sum_length, sum_length + 3)
            sum_length += 3
            self.format_info[f'{var_nam} – Code modulateur de lieu'] = (sum_length, sum_length + 2)
            sum_length += 2
            self.format_info[f'{var_nam} – Code modulateur de patient'] = (sum_length, sum_length + 2)
            sum_length += 2
            self.format_info[f'{var_nam} – Code modulateur de technicité'] = (sum_length, sum_length + 2)
            sum_length += 2
            self.format_info[f'{var_nam} – Code intervenant'] = (sum_length, sum_length + 2)
            sum_length += 2
            self.format_info[f'{var_nam} – Filler'] = (sum_length, sum_length + 1)
            sum_length += 1
            self.format_info[f'{var_nam} – Nombre de réalisations'] = (sum_length, sum_length + 2)
            sum_length += 2
            self.format_info[f'{var_nam} – Date de réalisation'] = (sum_length, sum_length + 8)
            sum_length += 8
            self.format_info[f'{var_nam} – Nombre réel de patients'] = (sum_length, sum_length + 2)
            sum_length += 2
            self.format_info[f'{var_nam} – Nombre d’intervenants'] = (sum_length, sum_length + 2)
            sum_length += 2
            self.format_info[f'{var_nam} – Extension Documentaire'] = (sum_length, sum_length + 2)
            sum_length += 2


        for i in range(self.dynamic_fields['CCAM']['count']):
            var_nam = f"CCAM-{i}"
            self.format_info[f'{var_nam} - Date de réalisation'] = (sum_length, sum_length + 8)
            sum_length += 8
            self.format_info[f'{var_nam} – Code CCAM'] = (sum_length, sum_length + 7)
            sum_length += 7
            self.format_info[f'{var_nam} – Extension PMSI'] = (sum_length, sum_length + 3)
            sum_length += 3
            self.format_info[f'{var_nam} – Code de la phase'] = (sum_length, sum_length + 1)
            sum_length += 1
            self.format_info[f'{var_nam} – Code de l\'activité'] = (sum_length, sum_length + 1)
            sum_length += 1
            self.format_info[f'{var_nam} – Extension documentaire'] = (sum_length, sum_length + 1)
            sum_length += 1
            self.format_info[f'{var_nam} – Nombre de réalisations'] = (sum_length, sum_length + 2)
            sum_length += 2

    def extract_info(self, text_line):
        self._update_dynamic_counts(text_line)
        self.generate_dynamic_fields_positions()
        info = {}

        for var_name, (start, end) in self.format_info.items():
            value = text_line[start:end] if start is not None and end is not None else "Not Found"
            info[var_name] = value

        return info


format_reader = DynamicFieldCSVReader('./assets/format_RHS-2023_jugu.csv')
rhs_file_path = './rhs/RHS_Groupe_20231019,1441.txt'
with open(rhs_file_path, 'r') as file:
    lines = file.readlines()  # Read the first line and strip newline characters

extracted_info = format_reader.extract_info(lines[100])
print(extracted_info)
