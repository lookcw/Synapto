import java.io.*;
import java.util.Random;

import au.com.bytecode.opencsv.CSVWriter;
import weka.classifiers.AbstractClassifier;
import weka.classifiers.Classifier;
import weka.classifiers.evaluation.Evaluation;
import weka.classifiers.trees.RandomForest;
import weka.core.Instances;
import weka.core.Utils;
import weka.core.converters.CSVLoader;

public class Results_Writer {

	public static void Results_Writer(String CSVFilePath,int seed,int folds) throws Exception {
		   CSVLoader loader = new CSVLoader();
		   loader.setSource(new File(CSVFilePath));
		
		   String[] options = new String[1]; 
		   options[0] = "";
		   // -H means no header
		   loader.setOptions(options);
		
		   Instances data = loader.getDataSet();
		   Random rand = new Random(seed);   // create seeded number generator
		   Instances randData = new Instances(data);   // create copy of original data
		   randData.randomize(rand);         // randomize data with number generator
		  RandomForest rf = new RandomForest();
		           
		   
		  randData.setClassIndex(randData.numAttributes() - 1);
		   
		    Evaluation eval = new Evaluation(randData);
		    
		    for (int n = 0; n < folds; n++) {
		         Instances train = randData.trainCV(folds, n);
		         Instances test = randData.testCV(folds, n);
		         // the above code is used by the StratifiedRemoveFolds filter, the
		         // code below by the Explorer/Experimenter:
		         // Instances train = randData.trainCV(folds, n, rand);
		 
		         // build and evaluate classifier
		         Classifier clsCopy = AbstractClassifier.makeCopy(rf);
		         clsCopy.buildClassifier(train);
		         eval.evaluateModel(clsCopy, test);
		         eval.evaluateModel(clsCopy, randData);
			        
		    }
		    
		    CSVWriter writer = new CSVWriter(new FileWriter("yourfile.csv"), '\t');
		    
		    
		    PrintWriter pw = new PrintWriter(new File("Weka_Results.csv"));
	        StringBuilder sb = new StringBuilder();
	        sb.append("=== Setup ===");
	        sb.append('\n');
	        
	        sb.append("Classifier: " + rf.getClass().getName() + " ");
	        sb.append(',');
	        sb.append(Utils.joinOptions(rf.getOptions()));
	        sb.append('\n');
	       
	        sb.append("Dataset: " + data.relationName());
	        sb.append('\n');
	        
	        sb.append("Folds: " + folds);
	        sb.append('\n');
	        
	        sb.append("Seed: " + seed);
	        sb.append("\r\n");
	        
	        sb.append(eval.toSummaryString("=== " + folds + "-fold Cross-validation ===", false));
	        sb.append(eval.toClassDetailsString());
	        sb.append(eval.toMatrixString());
	       
	        
	        pw.write(sb.toString());
	        pw.close();
	       


		}
		
		public static void main(String[] args ) throws Exception {
			Results_Writer("../../Synapto/tensorflow/Brazil/Feature_Sets/Fil_higARmin7.csv",0,10);
		}
	
	
	
}
