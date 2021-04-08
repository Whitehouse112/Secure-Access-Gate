from google.cloud import pubsub_v1

project_id = 'quiet-groove-306310',

def createTopic(uuid):
    
    topic_id = uuid

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    publisher.create_topic(request={"name": topic_path})

def publishTopic(uuid):
    
    topic_id = uuid

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    publisher.publish(topic_path, 'OpenGate')