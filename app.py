import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import sigmoid_kernel


from sqlConnect import connection_url;
from sqlalchemy import create_engine;


from flask import Flask, request, jsonify;



app = Flask(__name__)



def recommendation( job_id , location, serviceType, top_n = 5 ):
    

    #Sql queries
    query_services = f"select service_id,description from services where location = {location.ignoreCase()}, serviceType = {serviceType.ignoreCase()};"
    
    query_jobs = "select job_id,description from jobs;"
    engine = create_engine(connection_url)





    #get latest Data
    df_jobs = pd.read_sql(query_jobs, engine).drop_duplicates
    df_services = pd.read_sql(query_services, engine).drop_duplicates

    #tfid stop words as english
    tfidf = TfidfVectorizer(stop_words = 'english')

    df_jobs['description'] = df_jobs['description'].fillna("") # replacing Null and n/a values with an empty string to remove its effect */
    df_services['description'] = df_services['description'].fillna("") # replacing Null and n/a values with an empty string to remove its effect */
    
    combined_text = pd.concat([df_jobs['description'], df_services['description']])
    tfidf_matrix = tfidf.fit_transform(combined_text) # Vectorize text data using TF-IDF
    
    #spliting TF-IDF matrix into job descriptions and service description
    tfidf_matrix_jobs = tfidf_matrix[:len(df_jobs)]
    tfidf_matrix_services = tfidf_matrix[len(df_jobs):]


    #computing Cosine Similarity
    cosine_similarity_matrix = cosine_similarity(tfidf_matrix_jobs,tfidf_matrix_services)


    # Find the index of the job in the DataFrame
    job_index = df_jobs[df_jobs['job_id'] == job_id].index[0]
    # Get the top N recommendations for this job
    top_indices = np.argsort(cosine_similarity_matrix[job_index])[::-1][:top_n]
    recommended_contractors = df_services.iloc[top_indices]['service_id'].values
    return recommended_contractors

    

@app.route('/recommendations/<int:job_id>', methods=['GET'])
def recommendation(job_id):
    try:
        recommended_contractors = recommendation(job_id)
        return jsonify ({
            'job_id': job_id,
            'recommended_contractors': recommended_contractors.tolist()
        })
    except IndexError:
        return jsonify({'error': 'Job ID not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)