{
'name': 'CampOS Transportation Application',
'description': 'Manage your bus rides.',
'author': 'Doobi',
'depends': ['mail','campos_event','campos_preregistration'],
'application': True,
'data': ['views/webtourusneed_view.xml',
         'views/webtourusdestination_view.xml',
         'views/webtourparticipant_view.xml',
         'data/webtourusdestination_scheduler.xml',
         'security/ir.model.access.csv',],
}