from django.conf import settings
import joblib
import pandas as pd


class CosineSimPredictor:
    def __init__(self):
        path_base = str(settings.BASE_DIR)
        path_to_artifacts = path_base + "/research/"
        self.metadata = joblib.load(path_to_artifacts + "metadata.joblib")
        self.model = joblib.load(path_to_artifacts + "cosine_sim.joblib")

    def preprocessing(self, input_data):
        return input_data['tmdbId']

    def weighted_rating(self, x, m, C):
        v = x['vote_count']
        R = x['vote_average']
        return (v / (v + m) * R) + (m / (m + v) * C)

    def predict(self, tmdbId):
        # disable warning for cleaner output
        pd.set_option('mode.chained_assignment', None)

        indices = pd.Series(self.metadata.index, index=self.metadata['tmdbId'])
        if tmdbId not in indices:
            return 'tmdbId not found'
        index = indices[tmdbId]
        sim_scores = list(enumerate(self.model[index]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:26]
        movie_indices = [i[0] for i in sim_scores]

        movies = self.metadata.iloc[movie_indices][['tmdbId', 'title', 'vote_count', 'vote_average', 'release_date', 'poster_path', 'original_title']]
        vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
        vote_averages = movies[movies['vote_average'].notnull()]['vote_average'].astype('int')
        m = vote_counts.quantile(0.60)
        C = vote_averages.mean()
        qualified = movies[(movies['vote_count'] >= m) & (movies['vote_count'].notnull()) & (movies['vote_average'].notnull())]
        qualified.vote_count = qualified.vote_count.astype('int')
        qualified.vote_count = qualified.vote_count.astype('int')
        qualified['wr'] = qualified.apply(self.weighted_rating, args=(m, C,), axis=1)
        qualified = qualified.sort_values('wr', ascending=False).head(20)
        return qualified.to_dict('records')

    def postprocessing(self, result):
        '''
        returns:
            movies object - list of 10 recommendations in order (tmdbId, name, weighted rating for each)
            status

            {'movies': [
                {'tmdbId': 1873, 'title': 'The Dark Knight', 'wr': 7.830744},
                {'tmdbId': 200, 'title': 'The Joker', 'wr': 7.852230},
                ...
              ],
             'status': 'OK'
            }
        '''

        return {"movies": result, "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}
        return prediction
