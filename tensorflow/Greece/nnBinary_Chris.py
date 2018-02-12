import tensorflow as tf
import numpy as np
import csv
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2' #hide warnings

# Network Parameters
for ran in range(1):
    tf.set_random_seed(ran)
    learning_rate = 0.2
    n_hidden1 = 100 # 1st layer number of neurons
    n_hidden2 = 100 # 2nd layer number of neurons
    n_hidden3 = 100 # 3rd layer number of neurons
    n_input = 4816 # Data input
    n_classes = 2 # 0 - Healthy, 1 - AD
    num_folds = 10 #cross validation

    #declare interactive session
    sess = tf.InteractiveSession()

    X = tf.placeholder(tf.float32, shape=[None, n_input], name="x-input")
    Y = tf.placeholder(tf.float32, shape=[None, n_classes], name="y-input")

    W1 = tf.Variable(tf.random_normal([n_input, n_hidden1]), name="Weight1")
    W2 = tf.Variable(tf.random_normal([n_hidden1, n_hidden2]), name="Weight2")
    W3 = tf.Variable(tf.random_normal([n_hidden2, n_hidden3]), name="Weight3")
    W4 = tf.Variable(tf.random_normal([n_hidden3, n_classes]), name="Weight4")

    b1 = tf.Variable(tf.random_normal([n_hidden1]), name="Bias1")
    b2 = tf.Variable(tf.random_normal([n_hidden2]), name="Bias2")
    b3 = tf.Variable(tf.random_normal([n_hidden3]), name="Bias3")
    b4 = tf.Variable(tf.random_normal([n_classes]), name="Bias4")

    #forward-pass
    #hidden layer 
    H1 = tf.nn.sigmoid(tf.matmul(X, W1) + b1)
    H2 = tf.nn.sigmoid(tf.matmul(H1, W2) + b2)
    H3 = tf.nn.sigmoid(tf.matmul(H2, W3) + b3)
    #predicted values
    output = tf.nn.sigmoid(tf.matmul(H3, W4) + b4)

    #backward-pass
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=Y, logits=output))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate)
    train = optimizer.minimize(loss)

    #training set
    array_Y = []

    combined_HC = []
    combined_AD = []

    basepath = 'HC_stan'
    combined_HCs = []
    for filename in os.listdir(basepath):
        if filename.endswith('.csv'):
            with open(os.path.join(basepath, filename)) as f:
                reader = csv.reader(f)
                array = list(reader)
                array = np.array(array)
                #concatenate each electrode erp vector into one vector per instance
                Etotal = []
                for e in range(1,len(array.T)):
                    E = (array[:,e])
                    Etotal.extend(E)
                #add erp values of each instance
                combined_HCs.append(Etotal)
                #output = 0
                array_Y.extend([0])

    basepath = 'HC_targ'
    combined_HCt = []
    for filename in os.listdir(basepath):
        if filename.endswith('.csv'):
            with open(os.path.join(basepath, filename)) as f:
                reader = csv.reader(f)
                array = list(reader)
                array = np.array(array)
                #concatenate each electrode erp vector into one vector per instance
                Etotal = []
                for e in range(1,len(array.T)):
                    E = (array[:,e])
                    Etotal.extend(E)
                #add erp values of each instance
                combined_HCt.append(Etotal)
                
    for i in range(len(combined_HCs)):
        concat = []
        concat.extend(combined_HCs[i])
        concat.extend(combined_HCt[i])
        combined_HC.append(concat)
    combined_HC = np.array(combined_HC)

    basepath = 'AD_stan'
    combined_ADs = []
    for filename in os.listdir(basepath):
        if filename.endswith('.csv'):
            with open(os.path.join(basepath, filename)) as f:
                reader = csv.reader(f)
                array = list(reader)
                array = np.array(array)
                #concatenate each electrode erp vector into one vector per instance
                Etotal = []
                for e in range(1,len(array.T)):
                    E = (array[:,e])
                    Etotal.extend(E)
                #add erp values of each instance
                combined_ADs.append(Etotal)
                #output = 1
                array_Y.extend([1])
    basepath = 'AD_targ'
    combined_ADt = []
    for filename in os.listdir(basepath):
        if filename.endswith('.csv'):
            with open(os.path.join(basepath, filename)) as f:
                reader = csv.reader(f)
                array = list(reader)
                array = np.array(array)
                #concatenate each electrode erp vector into one vector per instance
                Etotal = []
                for e in range(1,len(array.T)):
                    E = (array[:,e])
                    Etotal.extend(E)
                #add erp values of each instance
                combined_ADt.append(Etotal)

    for j in range(len(combined_ADs)):
        concat = []
        concat.extend(combined_ADs[j])
        concat.extend(combined_ADt[j])
        combined_AD.append(concat)
    combined_AD = np.array(combined_AD)

    total = []
    total.extend(combined_HC)
    total.extend(combined_AD)

    X_data = np.array(total)

    array_Y = np.array(array_Y)
    #convert to one-hot arrays
    array_Y = array_Y.astype(int)
    Y_data = np.eye(n_classes)[array_Y]

    #controlled shuffle function
    def shuffle(input):
        np.random.seed(1)
        return np.random.shuffle(input)

    shuffle(X_data)
    shuffle(Y_data)

    #cross-validation 
    elements = len(X_data)
    train_X=[]
    train_Y=[]
    test_X=[]
    test_Y=[]
    total_accuracy = 0
    total_TP = 0
    #total_TN = 0
    total_FP = 0
    total_FN = 0
    total_Prec = 0
    total_Fmeasure = 0
    total_AUC = 0

    for i in range(0,num_folds):
        print("Fold Number:", i+1)
        
        Xdata = X_data
        Ydata = Y_data
        Xdata = np.array(Xdata)
        Ydata = np.array(Ydata)
        
        first_index=int((i*elements/float(num_folds)))
        second_index=int(((i+1)*elements/float(num_folds)))
        #print('first index',first_index)
        #print('second index',second_index)
        
        #split the sets into training and testing sets
        test_X = Xdata[first_index:second_index]
        test_Y = Ydata[first_index:second_index]
        index = [];
        for n in range(first_index,second_index):
            index.extend([n])
            
        Xdata = np.delete(Xdata,index,axis=0)
        Ydata = np.delete(Ydata,index,axis=0)
        train_X = Xdata
        train_Y = Ydata
        
        #train/test model
        init = tf.global_variables_initializer()
        sess.run(init)

        #cycles of all training set
        for epoch in range(1000):
            #train with each example
            for j in range(len(train_X)):
                sess.run(train, feed_dict={X: train_X[j:j+1], Y: train_Y[j:j+1]})
            
            if epoch == 999:
                print('Epoch ', epoch)
                #print('Train Prediction ', sess.run(output, feed_dict={X: train_X, Y: train_Y}))
                #print('Weight1 ', sess.run(w1))
                #print('Bias1 ', sess.run(b1))
                print('cost ', sess.run(loss, feed_dict={X: train_X, Y: train_Y}))
                
                train_prediction = tf.equal(tf.argmax(output, axis=1), tf.argmax(Y, axis=1))
                #calculate train accuracy
                train_accuracy = tf.reduce_mean(tf.cast(train_prediction, "float"))
                print("Train Accuracy:", train_accuracy.eval({X: train_X, Y: train_Y}))
                    
                    
        #test model
        #print('Test Prediction ', sess.run(output, feed_dict={X: test_X, Y: test_Y}))
        
        #confusion matrix
        labels = tf.argmax(test_Y, axis=1)
        predictions = tf.argmax(output.eval({X: test_X}), axis=1)
        
        matrix = sess.run(tf.confusion_matrix(labels,predictions))
        print(matrix)
        
        if(len(matrix) == 2):
            TN = float(matrix[0][0])
            FP = float(matrix[0][1])
            FN = float(matrix[1][0])
            TP = float(matrix[1][1])
            
        total = TN + FP + FN + TP
        actualNO = TN + FP
        actualYES = FN + TP
        predYES = FP + TP
        
        fold_accuracy = (TP + TN)/total
        print("Test Accuracy:", fold_accuracy)
        if(actualYES == 0):
            TPrate = 0
        else:
            TPrate = TP/actualYES

        print("Recall:", TPrate)
        #TNrate = TN/actualNO
        #print("True Negative:", TNrate)
        if(actualNO == 0):
            FPrate = 0
        else:
            FPrate = FP/actualNO

        print("False Positive:", FPrate)
        if(actualYES == 0):
            FNrate = 0
        else:
            FNrate = FN/actualYES

        print("False Negative:", FNrate)
        if(predYES == 0):
            Prec = 0
        else:
            Prec = TP/predYES

        print("Precision:", Prec)
        if((Prec+TPrate) == 0):
            Fmeasure = 0
        else:
            Fmeasure = (2*Prec*TPrate)/(Prec+TPrate)
        
        print("F-measure:", Fmeasure)
        
        auc = tf.metrics.auc(labels,
        predictions,
        weights=None,
        num_thresholds=200,
        metrics_collections=None,
        updates_collections=None,
        curve='ROC',
        name=None)
        
        tf.local_variables_initializer().run()
        AUC = sess.run(auc)
        print("ROC AUC:", AUC[1])
        
        #compute overall accuracy, false negative, and false positive
        total_accuracy += fold_accuracy*(float(len(test_X))/len(X_data))
        total_TP += TPrate*(float(len(test_X))/len(X_data))
        #total_TN += TNrate*(len(test_X)/len(X_data))
        total_FP += FPrate*(float(len(test_X))/len(X_data))
        total_FN += FNrate*(float(len(test_X))/len(X_data))
        total_Prec += Prec*(float(len(test_X))/len(X_data))
        total_Fmeasure += Fmeasure*(float(len(test_X))/len(X_data))
        total_AUC += AUC[1]*(float(len(test_X))/len(X_data))
        
            
    print("Overall Accuracy:", total_accuracy)
    print("Overall False Negative:", total_FN)
    print("Overall False Positive:", total_FP)
    print("Overall Precision:", total_Prec)
    print("Overall Recall:", total_TP)
    print("Overall F-measure:", total_Fmeasure)
    print("Overall ROC AUC:", total_AUC)
#print("Overall True Negative:", total_TN)