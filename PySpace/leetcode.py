#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List

def dailyTemperatures(temperatures: List[int]) -> List[int]:
        answer = [0]*len(temperatures)
        stack = []
        for i in range(len(temperatures)):
            while len(stack)>0 and temperatures[i] > temperatures[stack[-1]]:
                answer[stack[-1]] = i - stack[-1]
                stack.pop()
            stack.append(i)
        return answer



if __name__ == '__main__':
    print(dailyTemperatures([73,74,75,71,69,72,76,73]))
