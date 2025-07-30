from config.db import SessionLocal

try:
    db = SessionLocal()
    print("✅ Conexão com o banco de dados bem-sucedida!")
except Exception as e:
    print("❌ Erro ao conectar:", e)
finally:
    db.close()
