

class Parser:

    def __init__(self):
        pass

    def parse(data){
        html, js = ""
        for i in data:
            if 'object' in data and i['object']:
                html, js = self.get_get_object_data(data)

        return html, js
    }


    def get_object_data(self, data):
        html, js = None

        return html, js


    def get_input_data(self, data):
        html = "<input {0} >".format(" ".join([key + "='" + value + "'" for key, value in data.get('attrs', []) ])
        js = ""
        return html, js

    
    def get_select_data(self, data):
        attrs = " ".join([key + "='" + str(value) + "'" for key, value in data.get('attrs', []) ])
        options = "\n".join(["<option value='{0}'>{1}</option>".format(op[0], op[1]) for op in data.get('options', []))
        html = "<select {0}>{1}</select>".format(attrs, options)
        js = None
        if "on_select" in data:
            pass
        return html, js




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
                ('yes', 'beli'),
                ('no', 'xeyr')
            ],
            'on_select': {
                'yes': {
                    'object': True,
                    'multiple': True,
                    'type': 'div',
                    'attrs': {
                        'class': 'form-group',
                    },
                    'nodes': [
                        {
                            'object': False,
                            'multiple': False,
                            'attrs': { },
                            'type': 'input',
                        },
                    ]
                },
            }
        }
    ]
}


documents = {
    'nikah': {
        'applicant-name': {
            'object': False,
            'multiple':  False,
            'type': 'input',
            'attrs': {
                'type': 'text',
                'value': 'İddiaçı (Ad, Soyad, Ata adı)',
                'class': 'form-group',
                'id': 'applicant-name' 
            },
        },
        'applicant-gender': {
            'object': False,
            'multiple': False,
            'on_select': {
                'female': {
                    'object': True,
                    'multiple': False
                }
            }
        }
        'has-children': {
            'object': False,
            'multiple': False, 
            'on_select': {
                'Yes': {
                    'object':True,
                    'multiple': False,
                    ''
                    'nodes': {
                        ''
                    }
                }
            }
        }
    }
}
