
import java.util.*;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class FilterTweets {

	public static void main(String[] args) throws IOException {
		
		if (args[0] == null) return;
		String filename = args[0];
		
		BufferedReader br = new BufferedReader(new FileReader("movielist"));
		String line;
		
		ArrayList<Movie> movies = new ArrayList<Movie>();
		
		// create arraylist of movie object
		while((line = br.readLine()) != null){
			String[] splits = line.split("\\t");
			String name = splits[0];
			String moviePatternString = splits[1];
			int caseInsensitiveOption = Integer.valueOf(splits[2]);
			
			System.out.println(name + " : " + moviePatternString + " :" + splits[2]);
			
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
		Pattern p = Pattern.compile("\\{\"text\":\"(.*)\",\"contributors\".*\"coordinates\":.*\\}");

		Matcher m;
        String text = "";
 		String fullline ="";
        write(" { \"data\" : [" + "\n");
        while ((line = br.readLine()) != null) {
        	if (line.contains("????") || line.length() == 0 ) {
        		// skips when it matches on ????
        	} else {
        	
        		m = p.matcher(line);
        		
				while (m.find()) {         
					text= m.group(1);
        			fullline= m.group();
        		}

 				//print only text	
        		//write("text: "+ text +"\n"); 

                String newline="";
                Movie movie;
                boolean theFirstLine=true;
				for(int i=0;i<movies.size();i++){
                    movie = movies.get(i);
					Pattern pattern = movie.getPattern();	
					m = pattern.matcher(text);
					while (m.find()) { 
						//write("movie "+movie.getName() +"\n"+ text +"\n");

                        newline = fullline.substring(0,1) + "\"no\":" + i + ","+fullline.substring(1);
                        if(theFirstLine) { write(newline); theFirstLine = false;}
                        else  write(",\n"+newline); 
						movie.plusCount();
                        break;
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
    		if (fw == null)
    			fw = new FileWriter("movieFiltered.txt", false);
    		fw.write(s);
    	} catch (IOException e) {}
    }
    
    private static void endWrite() {
    	try {
    		fw.close();
    	} catch (IOException e) {}
    }

}

class Movie{
	
	private String name;
	private int	count; 
	private Pattern pattern;
	
	Movie(String _name){
		name = _name;
	}
	
	Movie(String _name, Pattern _pattern, int _count){
		name = _name;
		pattern = _pattern;
		count = _count;
	}
	
	String getName(){
		return name;
	}
	
	int getCount(){
		return count;
	}
	
	void plusCount(){
		count++;
	}
	
	void setPattern(Pattern _pattern){
		pattern = _pattern;
	}
	
	Pattern getPattern(){
		return pattern;
	}
	

	
}
