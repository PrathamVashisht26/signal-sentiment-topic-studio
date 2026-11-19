import io
import unittest
from app import app


class AnalysisTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_sample_and_assets(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        with self.client.get('/static/app.js') as response:
            self.assertEqual(response.status_code, 200)
        data = self.client.post('/api/analyze', json={'sample': True}).get_json()
        self.assertEqual(data['total'], 50)
        self.assertEqual(sum(data['counts'].values()), 50)
        self.assertEqual(sum(t['count'] for t in data['topics']), 50)

    def test_negation_and_duplicates(self):
        data = self.client.post('/api/analyze', json={'text':'This is good\nThis is not good\nThis is good'}).get_json()
        self.assertEqual(data['duplicates'], 1)
        self.assertEqual([r['sentiment'] for r in data['rows']], ['Positive', 'Negative'])

    def test_empty_and_invalid_input(self):
        for data in [[], [1], 'invalid', {'text':''}, {'text':[]}, {'text':'x'*5001}, {'text':'\n'.join(str(n) for n in range(1001))}]:
            self.assertEqual(self.client.post('/api/analyze', json=data).status_code, 400)

    def test_csv(self):
        response = self.client.post('/api/analyze', data={'file':(io.BytesIO(b'text\n"Great, really great"\nBad\n'), 'test.csv')})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['total'], 2)
        response = self.client.post('/api/analyze', data={'file':(io.BytesIO(b'wrong\nhi'), 'test.csv')})
        self.assertEqual(response.status_code, 400)

    def test_empty_vocabulary_and_upload_limit(self):
        response = self.client.post('/api/analyze', json={'text':'the and\n!!!'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['topics'], [])
        response = self.client.post('/api/analyze', data=b'x'*(2*1024*1024+1), content_type='application/json')
        self.assertEqual(response.status_code, 413)
        response.close()
        response.request.close()


if __name__ == '__main__':
    unittest.main()
