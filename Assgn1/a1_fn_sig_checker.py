'''a1_fn_sig_checker.py
Function signature checker, for Assignment 1, in
CSE 415, Winter 2020.
'''

import a1

print("Checking is_multiple_of_3")

for arg in [-6, -1, 0, 11, 18, 3.0]:
   answer = a1.is_multiple_of_3(arg)
   if not answer in [True, False]:
      print("Warning: your function is_multiple_of_3 returned a value of the wrong type.")

print("Checking next_prime")

for (arg, corr_ans) in [(1,2),(59,61),(1000,1009)]:
   answer = a1.next_prime(arg)
   if answer != corr_ans:
      print("Warning: your function next_prime did not come up with an expected answer.")

print("Checking empirical_probabilities")

result = a1.empirical_probabilities("http://ai.google")
prob_of_computer = result["computer"]
print("According to your code, the probability of finding the word 'computer' on a Google AI web page is ", prob_of_computer)
try:
  if prob_of_computer >= 1:
    print("Your value is too high.")
except:
  print("Your value doesn't seem to be a probability value, or even a number at all.")

  
print("""Finally, this is a reminder that your code should not print any answers or
other messages, after you have it debugged and ready to turn in.""")
