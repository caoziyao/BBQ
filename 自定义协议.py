
Reset
	����  Reset 
	
����
	���� DATA

�������
	���� FLAT(SUCCESS, FAILURE)
	
����
	���� 	W/R		Addr		Rem			TimeOut		DATA
			��д	�ڵ��ַ	Ŀ�ĵ�ַ	��ʱʱ��
Ӧ��
	���� 	W/R		Addr		Rem			ERR			DATA
			��д	�ڵ��ַ	Ŀ�ĵ�ַ	������

״̬�ϱ�
	����	
	
	
login ����
	form = {
		'cmd': 'login',
		'addr': ID,
		'timeout': 0,
		'password': bbq_passwd
	}
login Ӧ��
	form = {
		'cmd': 'login',
		'err': True/False
	}