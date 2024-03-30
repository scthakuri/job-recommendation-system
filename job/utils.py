from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from geopy.distance import geodesic
from job.models import Job

def recommend_jobs_with_skills_and_location(user_skills, user_location):
    """
    Recommends jobs based on user skills and location.
    Args:
        user_skills (str): User skills.
        user_location (str): User location in latitude,longitude format.
    Returns:
        list: Recommended jobs sorted by relevance, with unmatched jobs at the end.
    """
    job_data = Job.objects.all()
    
    user_skills = user_skills.lower()
    user_location = user_location.lower()
    
    job_skills = [job.skills_required.lower() for job in job_data]
    job_locations = [(job.company.location.lower(), job.company.lat, job.company.lng) for job in job_data]
    
    vectorizer = TfidfVectorizer()
    user_skills_vector = vectorizer.fit_transform([user_skills])
    job_skills_vectors = vectorizer.transform(job_skills)
    
    similarity_scores = cosine_similarity(user_skills_vector, job_skills_vectors).flatten()
    
    relevant_jobs = []
    unmatched_jobs = []
    for idx, job in enumerate(job_data):
        if similarity_scores[idx] > 0.5:
            user_lat, user_lng = map(float, user_location.split(','))
            job_location, job_lat, job_lng = job_locations[idx]
            job_distance = geodesic((job_lat, job_lng), (user_lat, user_lng)).kilometers
            if job_distance <= 50:
                relevant_jobs.append(job)
        else:
            unmatched_jobs.append(job)

    return relevant_jobs + unmatched_jobs


def recommend_jobs_with_location_only(user_location):
    """
    Recommends jobs based on user location only.
    Args:
        user_location (str): User location in latitude,longitude format.
    Returns:
        list: Recommended jobs sorted by relevance, with unmatched jobs at the end.
    """
    job_data = Job.objects.all()

    user_location = user_location.lower()

    job_locations = [(job.company.location.lower(), job.company.lat, job.company.lng) for job in job_data]

    relevant_jobs = []
    unmatched_jobs = []
    user_lat, user_lng = map(float, user_location.split(','))
    for idx, job in enumerate(job_data):
        job_location, job_lat, job_lng = job_locations[idx]
        job_distance = geodesic((job_lat, job_lng), (user_lat, user_lng)).kilometers
        if job_distance <= 50:
            relevant_jobs.append(job)
        else:
            unmatched_jobs.append(job)

    return relevant_jobs + unmatched_jobs


def recommend_jobs_with_skills_only(user_skills):
    """
    Recommends jobs based on user skills only.
    Args:
        user_skills (str): User skills.
    Returns:
        list: Recommended jobs sorted by relevance, with unmatched jobs at the end.
    """
    job_data = Job.objects.all()

    user_skills = user_skills.lower()

    job_titles = [job.title.lower() for job in job_data]
    job_skills = [job.skills_required.lower() for job in job_data]

    vectorizer = TfidfVectorizer()
    user_skills_vector = vectorizer.fit_transform([user_skills])
    job_skills_vectors = vectorizer.transform(job_skills)

    similarity_scores = cosine_similarity(user_skills_vector, job_skills_vectors).flatten()

    relevant_jobs = []
    unmatched_jobs = []
    for idx, job in enumerate(job_data):
        title_similarity = cosine_similarity(vectorizer.transform([user_skills]), vectorizer.transform([job.title.lower()])).flatten()[0]
        if similarity_scores[idx] > 0.5 or title_similarity > 0.5:
            relevant_jobs.append(job)
        else:
            unmatched_jobs.append(job)

    return relevant_jobs + unmatched_jobs


def get_related_jobs(job_id):
    """
    Get related jobs based on the similarity of job titles and descriptions.
    Args:
        job_id (int): ID of the current job.
    Returns:
        list: Related jobs sorted by relevance, with unmatched jobs at the end.
    """
    current_job = Job.objects.get(id=job_id)
    current_title = current_job.title.lower()
    current_description = current_job.description.lower() if current_job.description else ""

    all_jobs = Job.objects.exclude(id=job_id)

    job_texts = [f"{job.title.lower()} {job.description.lower() if job.description else ""}" for job in all_jobs]
    
    vectorizer = TfidfVectorizer()
    job_texts_vector = vectorizer.fit_transform([f"{current_title} {current_description}"] + job_texts)

    similarity_scores = cosine_similarity(job_texts_vector)[0][1:]

    related_jobs = sorted(zip(all_jobs, similarity_scores), key=lambda x: x[1], reverse=True)
    sorted_job_objects = [job for job, _ in related_jobs]
    return sorted_job_objects + [job for job in all_jobs if job not in sorted_job_objects]
