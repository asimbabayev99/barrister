

class Parser:

    def __init__(self):
        pass

    def parse(self, data):
        result_html = ""
        result_js = ""
        for i in data:
            if i.get('object', False):
                if i.get('multiple', False):
                    html, js = self.get_table_object_data(i)
                else:
                    html, js = self.get_object_data(i)
            else:
                if i.get('type') == 'input':
                    html, js = self.get_input_data(i)
                elif i.get('type') == 'select':
                    html, js = self.get_select_data(i)
                else:
                    raise Exception("Unknown data type")
            result_html += html
            result_js += js
        return result_html, result_js


    def get_table_object_data(self, data):
        # id of current object
        id = data.get('attrs').get('id')
        if not id:
            raise Exception("Object(multiple) type must have id in attrs")
        # join attributes of this object
        attrs = " ".join([key + "='" + str(value) + "'" for key, value in data.get('attrs', []).items() ])
        # get content for child elements
        content, js = self.parse(data.get('nodes', []))
        # build table heads with placeholders in node objects
        ths = "\n".join(["<th>" + i['attrs']['placeholder'] + "</th>" for i in data.get('nodes', []) ])
        # make table and html content for this object
        table = "<table><thead><tr>{0}</tr></thead><tbody id=\"table_{1}\"></table>".format(ths, id)
        add_button = "<input type=\"button\" value='Əlavə et' id=\"add_{0}\">".format(id)
        html = "<div {0}>\n{1}\n{2}\n{3}</div>".format(attrs, table, content, add_button)

        # create javascript

        # remove row from table js
        remove_js = "$('.delete_" + id + "').click(function(){" + "$(this).parents('tr').remove();})\n"

        # build varibles and row to append to the table  
        vars = []
        row = "\"<tr>"
        for i in data.get('nodes', []):
            node_class = i['attrs']['class']
            node_name = i['attrs']['name']
            vars.append("var {0} = $('#{1}').val();".format(node_name, node_class))
            row += "<td class='{0}'>\" + {1} + \"</td>".format(node_class, node_name)
        row += "<td><button class='btn btn-danger delete_{0}'>Sil</button></td></tr>\"".format(id)
        vars = "\n".join(vars)

        # add js 
        js = "$('#add_" + id + "').on('click', function(){" + vars +  "$('#table_" + id + "').append(" + row + ");\n"
        js += remove_js + "});"
            
        return html, js

        



    def get_object_data(self, data):
        attrs = " ".join([key + "='" + str(value) + "'" for key, value in data.get('attrs', []).items() ])
        content, js = self.parse(data.get('nodes', []))
        html = "<div {0}>\n{1}</div>".format(attrs, content)
        return html, js


    def get_input_data(self, data):
        html = "<input {0} >\n".format(" ".join([key + "='" + str(value) + "'" for key, value in data.get('attrs', {}).items() ]) )
        js = ""
        return html, js

    
    def get_select_data(self, data):
        select_id = data.get('attrs', {}).get('id')
        # if not select_id:
        #     raise Exception('Id not found for select element')
        attrs = " ".join([key + "='" + str(value) + "'" for key, value in data.get('attrs', {}).items() ])
        options = "\n".join(["\t<option value='{0}'>{1}</option>".format(op[0], op[1]) for op in data.get('options', []) ])
        html = "<select {0}>\n{1}</select>\n".format(attrs, options)

        temp = []
        for key, value in data.get('on_select', {}).items():
            id = value.get('attrs', {}).get('id')
            if not id:
                raise Exception('Id not found (select statement)')
            temp.append((
                key, 
                "$(\"#" + id + "\").css(\"display\",\"none\");\n",
                "$(\"#" + id + "\").css(\"display\",\"block\");\n",
            ))

        # create swith statement denending on choosen option
        switch = "switch(val){\n"
        for key, value in data.get('on_select', {}).items():
            case = "\tcase '{0}':\n\t".format(key)
            for i in temp:
                if i[0] == key:
                    case += i[2]
                else:
                    case += i[1]
            switch = switch + case + "\tbreak;\n"
        default_case = "default: \n" + "\n".join([i[1] for i in temp]) + "break;\n"
        switch += default_case + "}"

    
        if data.get('on_select'):
            # selected value
            val = "\tval = $('#{0}').val();\n".format(select_id)
            js = "$('#" + select_id + "').on('change', function(){\n" + val + switch + "});"
        else:
            js = ""

        for key, value in data.get('on_select', {}).items():
            h, j = self.parse([value,])
            html += h
            js += j

        return html, js


    def get_json(self, data):
        js = ""
        results = []
        for i in data:  
            # for input type we just return name and value  
            if i['type'] == "input":
                name = i['attrs']['name']
                id = i['attrs']['id']
                result = "'{0}': $('#{1}').val()\n".format(id, name)
                results.append(result)
            # for select type we return val and depends on selected value content
            elif i['type'] == "select":
                result = "'{0}':$('#{1}').val()".format(i['attrs']['name'], i['attrs']['id'])
                if i.get('on_select'):
                    for key, value in i['on_select'].items():
                        j, r = self.get_json([value,])
                        js += j
                        results.append(",".join(r))
                results.append(result)
            # for object type we return result with recursive calling of his childs
            # and if it is multiple object type than we collect also data in table
            elif i.get('object'):
                if i['multiple']:
                    # dict variable for js
                    temp_js = "var {0} = [];\n".format(i['attrs']['id'])
                    # cols - key, value for each row
                    cols = []
                    for node in i['nodes']:
                        cols.append("'{}': $(this).find('.{}').text()\n".format(node['attrs']['name'], node['attrs']['class']))
                    cols = ",".join(cols)

                    # loop through each row in table 
                    loop = "$('#table_{0} tr').each(function()".format(i['attrs']['id']) + "{\n"
                    loop += "" + i['attrs']['id'] + ".push({" + cols + "});\n"
                    loop += "});\n"

                    # build result 
                    result = "'{0}':{0}".format(i['attrs']['id'])
                    js = temp_js + loop
                    results.append(result)
                else:
                    nodes = data.get('nodes', [])
                    j, r = self.get_json(nodes)
                    js += j
                    results.append(r)
        return js, results


    
    def submit_info(self, data):

        submit_button = "<button class='' id='submit_button' type='submit' value='Confirm' >"
        js, res = self.get_json(data)
        result = "$('#submit_button').on('click', function() {"
        result += js
        result += "var data = {" + ",".join(res) + "}"
        result += "});"

        return result






documents = {
    'nikah': [
        {
            'object': False,
            'multiple': False,
            'type': 'input',
            'attrs': {
                'class': 'form-group',
                'name': 'applicant-name',
                'type': 'text',
                'id': 'applicant-name',
            }
        },
        {
            'object': False,
            'multiple': False,
            'type': 'select',
            'options': [
                ('', 'Secin'),
                ('male', 'kisi'),
                ('female', 'qadin')
            ],
            'attrs': {
                'class': 'form-group',
                'name': 'applicant-gender',
                'id': 'applicant-gender',
            }
        },
        {
            'object': False,
            'multiple': False, 
            # 'block': True,
            'type': 'select',
            'options': [
                ('', 'Secin'),
                ('yes', 'beli'),
                ('no', 'xeyr')
            ],
            'attrs': {
                'name': 'has_children',
                'id': 'has_children'
            },
            'on_select': {
                'yes': {
                    'object': True,
                    'multiple': True,
                    'type': 'div',
                    'attrs': {
                        'id': 'child',
                        'class': 'form-group',
                        'style': 'display: none;'
                    },
                    'nodes': [
                        {
                            'object': False,
                            'multiple': False,
                            'attrs': { 
                                'name': 'child_name',
                                'id': 'child_name',
                                'class': 'child_name',
                                'type': 'text',
                                'placeholder': 'Adi'
                            },
                            'type': 'input',
                        },
                        {
                            'object': False,
                            'multiple': False,
                            'attrs': {
                                'name': 'child_gender',
                                'id': 'child_gender',
                                'class': 'child_gender',
                                'placeholder': 'Cinsi',
                            },
                            'type': 'select',
                            'options': [
                                ('', 'Secin'),
                                ('male', 'kisi'),
                                ('female', 'qadin')   
                            ]
                        }
                    ]
                },
            }
        }
    ]
}



parser = Parser()
html, js = parser.parse(documents['nikah'])
json = parser.submit_info(documents['nikah'])
# print(json)
js = "<script>\n" + js + "\n" + json + "\n</script>"
# print(html)
print(js)
