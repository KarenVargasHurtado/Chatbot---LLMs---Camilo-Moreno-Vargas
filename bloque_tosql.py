from llama_index.llms.ollama import Ollama
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.core import SQLDatabase
from sqlalchemy import create_engine, MetaData, Table, select
import torch
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from transformers import AutoModel, AutoTokenizer
#from llama_index import LLamaIndex, SimpleDirectoryReader, ServiceContext

# Datos de conexión
db_host = "localhost"
db_name = "idempiere"
db_user = "adempiere"
db_password = "adempiere"
db_port = "5432"

def get_engine():
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(connection_string)

# Definir la función get_sql_database antes de usarla
def get_sql_database(engine):
    return SQLDatabase(engine)

# Crear el engine
engine = get_engine()
metadata = MetaData()  # Solo inicializa una vez

# Inicializar Ollama
llm = Ollama(model="llama3.2:1b", request_timeout=120.0)
sql_database = get_sql_database(engine)

# Definir la tabla a_asset
ad_user = Table('ad_user', metadata, autoload_with=engine, schema='adempiere')

# Consulta
stmt = select(
    ad_user.c.ad_user_id,
    ad_user.c.ad_client_id,
    ad_user.c.ad_org_id,
    ad_user.c.isactive,
    ad_user.c.created,
    ad_user.c.createdby,
    ad_user.c.updated,
    ad_user.c.updatedby,
    ad_user.c.name,
    ad_user.c.description,
    ad_user.c.password,
    ad_user.c.email,
    ad_user.c.supervisor_id,
    ad_user.c.c_bpartner_id,
    ad_user.c.processing,
    ad_user.c.emailuser,
    ad_user.c.emailuserpw,
    ad_user.c.c_bpartner_location_id,
    ad_user.c.c_greeting_id,
    ad_user.c.title,
    ad_user.c.comments,
    ad_user.c.phone,
    ad_user.c.phone2,
    ad_user.c.fax,
    ad_user.c.lastcontact,
    ad_user.c.lastresult,
    ad_user.c.birthday,
    ad_user.c.ad_orgtrx_id,
    ad_user.c.emailverify,
    ad_user.c.emailverifydate,
    ad_user.c.notificationtype,
    ad_user.c.isfullbpaccess,
    ad_user.c.c_job_id,
    ad_user.c.ldapuser,
    ad_user.c.connectionprofile,
    ad_user.c.value,
    ad_user.c.userpin,
    ad_user.c.isinpayroll,
    ad_user.c.ad_user_uu,
    ad_user.c.ismenuautoexpand,
    ad_user.c.salt,
    ad_user.c.islocked,
    ad_user.c.dateaccountlocked,
    ad_user.c.failedlogincount,
    ad_user.c.datepasswordchanged,
    ad_user.c.datelastlogin,
    ad_user.c.isnopasswordreset,
    ad_user.c.isexpired,
    ad_user.c.securityquestion,
    ad_user.c.answer,
    ad_user.c.issaleslead,
    ad_user.c.c_location_id,
    ad_user.c.leadsource,
    ad_user.c.leadstatus,
    ad_user.c.leadsourcedescription,
    ad_user.c.leadstatusdescription,
    ad_user.c.c_campaign_id,
    ad_user.c.salesrep_id,
    ad_user.c.bpname,
    ad_user.c.bp_location_id,
    ad_user.c.isaddmailtextautomatically,
    ad_user.c.r_defaultmailtext_id,
    ad_user.c.ad_image_id,
    ad_user.c.isnoexpire,
    ad_user.c.issupportuser,
    ad_user.c.isbillto,
    ad_user.c.isshipto,
    ad_user.c.isvendorlead,
).select_from(ad_user)


# Ejecutar la consulta
with engine.connect() as connection:
    results = connection.execute(stmt).fetchall()
    print(results)

    from sqlalchemy import text

with engine.connect() as con:
    rows = con.execute(text("SELECT name FROM ad_user"))
    for row in rows:
        print(row)



#tokenizer de Hugging Face
model_name = "sentence-transformers/all-MiniLM-L6-v2"
hf_model = AutoModel.from_pretrained(model_name)
hf_tokenizer = AutoTokenizer.from_pretrained(model_name)

#embedding de Hugging Face
hf_embedding = HuggingFaceEmbedding(model_name=model_name)
        
#embedding local
#service_context = ServiceContext.from_defaults(embed_model=hf_embedding)

"""
query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database, tables=["ad_user"], llm=llm

)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
embeddings = embed_model.get_text_embedding("Which user was created first?")
print(len(embeddings))
print(embeddings[:5])
query_str = "Which user was created first?"
response = query_engine.query(query_str)"""

