//package flickoh;

import java.util.*;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.lang.String;

public class FilterTweets {
	
	static public String fn;

	public static void main(String[] args) throws IOException {
		
		if (args[0] == null) return;
		String filename = args[0];
		fn = filename;
		
		BufferedReader br = new BufferedReader(new FileReader("movielist"));
		String line;
		
		ArrayList<Movie> movies = new ArrayList<Movie>();
		
		// create arraylist of movie object
		while((line = br.readLine()) != null){
			String[] splits = line.split("\\t");
			String name = splits[0];
			String moviePatternString = splits[1];
			int caseInsensitiveOption = Integer.valueOf(splits[2]);
			
			//System.out.println(name + " : " + moviePatternString + " :" + splits[2]);
			
			Pattern pattern;
			switch (caseInsensitiveOption){
				case 0:
					pattern = Pattern.compile(moviePatternString,Pattern.CASE_INSENSITIVE | Pattern.UNICODE_CASE);
					break;
				case 1:
					pattern = Pattern.compile(moviePatternString);
					break;
				default:
					pattern = Pattern.compile(moviePatternString,Pattern.CASE_INSENSITIVE | Pattern.UNICODE_CASE);
			} 

			movies.add(new Movie(name, pattern, 0));
		}
		
	    br.close();
        	
		br = new BufferedReader(new FileReader(filename));
		//Pattern p = Pattern.compile("\"text\":\"(.*)\",\"[a-zA-Z]*\":");
		Pattern p = Pattern.compile("\"text\":\"(((?!\"[a-zA-Z]*\":).)*)\",\"[a-zA-Z_]*\":");

		Matcher m;
        String text = "";
        write(" { \"data\" : [" );
        boolean theFirstLine=true;
        while ((line = br.readLine()) != null) {
        	if (line.contains("????") || line.length() == 0 ) {
        		// skips when it matches on ????
        	} else {
        	
        		m = p.matcher(line);
        		
				if(m.find()) {         
					text= m.group(1);
                    //System.out.println("text: " + text);
        		}

                String newline="";
                Movie movie;
                //boolean theFirstLine=true;
				for(int i=0;i<movies.size();i++){
                    movie = movies.get(i);
					Pattern pattern = movie.getPattern();	
					m = pattern.matcher(text);
					if (m.find()) { 
						//write("movie "+movie.getName() +"\n"+ text +"\n");

                        newline = line.substring(0,1) + "\"no\": " + i + ","+line.substring(1, line.length()-1);
                        if(theFirstLine) { write("\n"+newline); theFirstLine = false;}
                        else  write(",\n"+newline); 
						movie.plusCount();
					}
				}
        	}
        }

        write("]}"+"\n");
		for(Movie movie: movies){
			System.out.println(movie.getName()+":"+movie.getCount());
		}

        endWrite();
		br.close();
        System.out.println("done!");

	}
	
	static FileWriter fw;
    
    private static void write(String s) {
    	try {
    		if (fw == null) {
    			//fw = new FileWriter("movieFiltered.txt", false);
    			//String [] temp = fn.split("\\"); 
    			String temp = "filtered_" + fn.substring(fn.lastIndexOf(92)+1);			
    			fw = new FileWriter(temp, false);
    		}
    		fw.write(s);
    	} catch (IOException e) {}
    }
    
    private static void endWrite() {
    	try {
    		fw.close();
    	} catch (IOException e) {}
    }

}

