conda activate /home/mostafizt/miniconda3/envs/tahsin
ngrok http 8501
ssh -R 80:localhost:8501 serveo.net
streamlit run app.py