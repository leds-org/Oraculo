import requests
import mysql.connector
from decouple import config
import datetime

# Configurações
DISCORD_WEBHOOK_URL = config('DISCORD_WEBHOOK_URL')
DB_CONFIG = {
    "host": config("DB_HOST"),
    "port": int(config("DB_PORT")),
    "user": config("DB_USER"),
    "password": config("DB_PASSWORD"),
    "database": config("DB_NAME")
}

# Função para enviar mensagens ao Discord
def post_to_discord(content):
    data = {"content": content}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Mensagem enviada com sucesso ao Discord!")
    else:
        print(f"Falha ao enviar mensagem: {response.status_code}, {response.text}")

# Conectar ao banco de dados
def fetch_issues(query):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Data limite das últimas 24 horas
limit_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')

queries = {
    "Issues sem descrição": f"""
        SELECT status, title, priority, original_type, creator_name, assignee_name, lead_time_minutes, url, resolution_date, created_date, updated_date
        FROM lake.issues
        WHERE (description IS NULL OR description = '' OR description = 'null')
        AND created_date >= '{limit_date}';
    """,
    "Issues sem tipo": f"""
        SELECT status, title, description, priority, creator_name, assignee_name, lead_time_minutes, url, resolution_date, created_date, updated_date
        FROM lake.issues
        WHERE (original_type IS NULL OR original_type = '')
        AND created_date >= '{limit_date}';
    """,
    "Issues sem responsável": f"""
        SELECT status, title, description, priority, original_type, creator_name, lead_time_minutes, url, resolution_date, created_date, updated_date
        FROM lake.issues
        WHERE (assignee_name IS NULL OR assignee_name = '')
        AND created_date >= '{limit_date}';
    """
}

for issue_type, query in queries.items():
    issues = fetch_issues(query)
    if issues:
        discord_message = f"**{issue_type}:**\n\n"
        for issue in issues:
            message_content = (
                f"- **Título**: {issue['title']}\n"
                f"  - **Status**: {issue['status']}\n"
                f"  - **Prioridade**: {issue['priority']}\n"
                f"  - **Criador**: {issue['creator_name']}\n"
                f"  - **Responsável**: {issue.get('assignee_name', 'N/A')}\n"
                f"  - **Criado em**: {issue['created_date']}\n"
                f"  - [Link]({issue['url']})\n\n"
            )
            if len(discord_message + message_content) >= 2000:
                post_to_discord(discord_message)
                discord_message = message_content
            else:
                discord_message += message_content

        post_to_discord(discord_message)
    else:
        post_to_discord(f"Nenhuma {issue_type.lower()} encontrada nas últimas 24 horas.")
