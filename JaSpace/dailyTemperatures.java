package JaSpace;

import java.util.Deque;
import java.util.LinkedList;

public class dailyTemperatures {
    public int[] dailyTemperatures(int[] temperatures) {
        int lens=temperatures.length;
        int []res=new int[lens];
        Deque<Integer> stack=new LinkedList<>();
        for(int i=0;i<lens;i++){

           while(!stack.isEmpty()&&temperatures[i]>temperatures[stack.peek()]){
                    res[stack.peek()]=i-stack.peek();
                    stack.pop();
                }
                stack.push(i);
        }

        return  res;
    }

    public static void main(String[] args) {
        int[]temperatures={73,74,75,71,69,72,76,73};
        dailyTemperatures dailyTemperatures=new dailyTemperatures();
        int[]res=dailyTemperatures.dailyTemperatures(temperatures);
        for(int i:res){
            System.out.println(i);
        }

    }
}
