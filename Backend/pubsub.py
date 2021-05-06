from google.cloud import pubsub_v1

project_id = 'quiet-groove-306310'

class PubSub():
    def createTopic(self, uuid):
        
        try:
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(project_id, uuid)
            publisher.create_topic(request={"name": topic_path})
            return None
        except Exception as e:
            return 500

    def publishTopic(self, uuid):
        
        topic_id = uuid

        try:
            data = bytes(topic_id, 'utf-8')
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(project_id, topic_id)
            publisher.publish(topic_path, data)
            return None
        except Exception as e:
            return 500