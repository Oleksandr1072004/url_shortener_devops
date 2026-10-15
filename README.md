| Параметр |	Опис |	Default |
|---|---|---|
| replicaCount |	Кількість реплік |	2 |
| image.repository |	Репозиторій образу |	api-gateway |
| image.tag |	Тег образу |	1.0.0 |
| service.type |	Тип сервісу |	NodePort |
| ingress.enabled |	Увімкнути Ingress |	false |
| config.baseUrl |	Базовий URL	| http://url-shortener.local |
| config.codeLength |	Довжина коду	| 6 |
| secret.databaseUrl |	Рядок підключення до БД	| (base64) |
