from flask import current_app
import secrets
import time
import json

# Función donde se agregan los datos a la cola de la base de datos de Redis.
def add_element_to_queue(queueName, periodicity, metadata, isPublish):
    """
    Add element to the queue
    Parameters
    ----------
    queueName:
        The name which the queue will be created.
        Accept values: MINUTES, HOURS, DAILY, WEEK, MONTHLY, YEARLY
    periodicity:
        The time to execute the queue.
    metadata:
        Extra information from the task.
    isPublish:
        True if the message will be published.
    Example:
    -------
        add_element_to_queue("MINUTES","5","For execute queue every 5 minutes.", True)
        add_element_to_queue("HOUR","10","For execute queue every hour with 10 minutes.", True)
        add_element_to_queue("DAILY","10:15","For execute queue every day at 10:15 AM.", True)
        add_element_to_queue("WEEK","10:15","For execute queue every week at 10:15 AM.", True)
        add_element_to_queue("MONTHLY","15;10:15","For execute queue every month, on the 15th at 10:15 AM.", True)
        add_element_to_queue("YEARLY","15;6;10:15","For execute every year in month 6, on the 15th at 10:15 AM.", True)
    Returns
    -------
    queueIdentifier: str
        Unique identifier of the queue created
    """
    # Datos a ingresar.
    identifier = secrets.token_hex()
    process= {"queueName":queueName, "identifier":identifier, "periodicity":periodicity, "metadata":metadata}
    current_app.logger.info("Subscriptores de la cola: %s" % process)
    if isPublish:
        s = current_app.redis.publish(queueName,json.dumps(process).encode("utf-8"))
        current_app.logger.info("Subscriptores de la cola: %s" % s)
    
    #Insertando mensaje en la cola.
    current_app.redis.hset(queueName,identifier,json.dumps(process).encode("utf-8"))

    return identifier

def remove_element_from_queue(queueName,elementIdentifier):
    """
    Remove element from the queue with the elementIdentifier parameter.
    Parameters
    ----------
    queueName
        the name of the queue where the element will be removed
    elementIdentifier:
        The unique element identifier.
    Returns
    -------
    The item to remove from the queue.
    """
    #publicando mensaje de borrado.
    process = {"queueName":'DELETE',"identifier":elementIdentifier}
    s = current_app.redis.publish("DELETE",json.dumps(process).encode("utf-8"))

    #Eliminando mensaje de la cola.
    current_app.redis.hdel(queueName,elementIdentifier)
    
    current_app.logger.info("Subscriptores de la cola: %s" % s)

def get_element_by_identifier(queueName,elementIdentifier):
    """
    Retrieve the element of the queue with the provided identifier.
    Parameters
    ----------
    queueName
        The name of the queue.
    elementIdentifier
        The unique element identifier.
    Returns
    ------
    The element in the queue.
    """
    result = current_app.redis.hget(queueName,elementIdentifier)
    return result

def get_all_elements_by_queue_name(queueName):
    """
    Retrieve all elements of a queues by queue name.
    Parameters
    ----------
    queueName
        The name of the queue.
    Returns
    -------
    The all elements in the queue.
    """
    result = current_app.redis.hgetall(queueName)
    return result

    #if __name__ == '__main__':
        #identifier = addElementQueue("MINUTE","1","{bot_id:2,bot_name='demo'}",True)
        #identifier = addElementQueue("HOUR","10","{bot_id:1,bot_name='demo'}",True)
        #identifier = addElementQueue("DAY","10:15","{bot_id:1,bot_name='demo'}",True) #Todos los días
        ##print(identifier)
        ##removeElementQueue("HOUR",'a0b443ac8d0143b6d7061b86787394ad88b8c6899d2c8312f5036480c77279dd')
        ##identifier = addElementQueue("DAY","10:15","{bot_id:1,bot_name='demo'}",True) #Todos los días
        #identifier = addElementQueue("WEEK","sunday,monday;10:15","{bot_id:1,bot_name='demo'}",True)

        #identifier = addElementQueue("MONTHLY","11;15:41","{bot_id:1,bot_name='demo'}",True)
        #identifier = addElementQueue("YEARLY","11;7;14:35","{bot_id:1,bot_name='demo'}",True)