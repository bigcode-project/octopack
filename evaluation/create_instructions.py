import re

def python_instruct(ex):
    '''
    Prompt example:
    from typing import List


    def has_close_elements(numbers: List[float], threshold: float) -> bool:
        """ Check if in given list of numbers, are any two numbers closer to each other than
        given threshold.
        >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
        False
        >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
        True
        """
    '''
    prompt = ex["prompt"]
    function_name = ex["entry_point"]

    number_of_def = len(re.findall(r"def ", prompt))
    if number_of_def >= 1:   
        idx = prompt.rfind("def ")
        prefix = prompt[0:idx]
        function = prompt[idx:]
    else:
        raise ValueError("This example does not have a function declaration.")
    splits = re.split("(\"{3}|\'{3})", function)
    if len(splits) != 5: # Before """, """, in-between, """, after """
        raise ValueError("Error in splitting function declaration.")
    
    left, middle, _ = splits[0], splits[2], splits[4]
    docstring = "\n".join([x.strip() for x in middle.split("\n") if x.strip()])
    signature = left[len("def "):].strip().strip(":")
    context = re.sub(r'^\s+|\s+$', '', prefix)+"\n"+re.sub(r'^\s+|\s+$', '',left)

    ex["signature"] = signature
    ex["docstring"] = docstring
    #ex["context"] = context
    ex["instruction"] = f"Write a Python function `{signature}` to solve the following problem:\n{docstring}"
    
    return ex


def cpp_instruct(ex):
    """
    Prompt example:
    /*
    Check if in given vector of numbers, are any two numbers closer to each other than
    given threshold.
    >>> has_close_elements({1.0, 2.0, 3.0}, 0.5)
    false
    >>> has_close_elements({1.0, 2.8, 3.0, 4.0, 5.0, 2.0}, 0.3)
    true
    */
    #include<stdio.h>
    #include<vector>
    #include<math.h>
    using namespace std;
    bool has_close_elements(vector<float> numbers, float threshold){
    """
    prompt = ex["prompt"]
    function_name = ex["entry_point"]

    lines = [line.strip() for line in prompt.split("\n") if line.strip()]
    function = None
    for idx, line in enumerate(reversed(lines)):
        if (function_name in line) and (line.strip().endswith("{")):
            function = line
            break
    if function is None:
        raise ValueError(f"Could not find function declaration. Prompt: {prompt} Function: {function_name}")

    signature = function.strip("{")
    splits = re.split("(\/\*|\*\/)", prompt)
    # Before \*, \*, in-between, \*, after \*
    if len(splits) < 5:
        # Maybe uses // instead of /* */
        is_comment = False
        comment_lines = []
        for line in reversed(lines):
            if line.strip().startswith("//"):
                is_comment = True
                comment_lines.append(line.strip("//").strip())
            # New comment that is not part of the function
            elif is_comment:
                break
        docstring = "\n".join([x.strip() for x in reversed(comment_lines) if x.strip()])
    else:
        left, middle, _ = splits[-5], splits[-3].strip("*"), splits[-1]
        docstring = "\n".join([x.strip() for x in middle.split("\n") if x.strip()])
    ex["signature"] = signature
    ex["docstring"] = docstring
    # ex["context"] = context
    ex["instruction"] = f"Write a C++ function `{signature}` to solve the following problem:\n{docstring}"

    return ex


def java_instruct(ex):
    """
    Prompt example:
    import java.util.*;
    import java.lang.*;

    class Solution {
        /**
        Check if in given list of numbers, are any two numbers closer to each other than given threshold.
        >>> hasCloseElements(Arrays.asList(1.0, 2.0, 3.0), 0.5)
        false
        >>> hasCloseElements(Arrays.asList(1.0, 2.8, 3.0, 4.0, 5.0, 2.0), 0.3)
        true
        */
        public boolean hasCloseElements(List<Double> numbers, double threshold) {
    """
    prompt = ex["prompt"]
    function_name = ex["entry_point"]

    lines = [line.strip() for line in prompt.split("\n") if line.strip()]
    function = lines[-1]
    signature = function.strip("{").strip()
    splits = re.split("(\/\*|\*\/)", prompt)

    # Before \*, \*, in-between, \*, after \*
    assert len(splits) >= 5, f"Error in splitting function declaration. Prompt: {prompt} Splits: {str(splits)}"
    
    # In case there are multiple appearances of /* and */ in the prompt index from behind
    # Strip * in case of /** */
    left, middle, _ = splits[-5], splits[-3].strip("*"), splits[-1]

    # This is imperfect & loses some implicit structure in the newlines
    # Good model should be able to do it without removing the newlines
    """
    lines = [line.strip() for line in middle.split("\n") if line.strip()]
    merged = []
    for line in lines:
        if len(merged) == 0:
            merged.append(line)
        else:
            if (merged[-1][-1].isalpha() or merged[-1].endswith((".", ","))) and not(line.startswith(("-",">",function_name,"Example","example","'.","'o","4.0","0.0"))):
                last = merged.pop()
                merged.append(last + " " + line)
            else:
                merged.append(line)
    
    docstring = "\n".join(merged)
    """
    docstring = "\n".join([x.strip() for x in middle.split("\n") if x.strip()])

    ex["signature"] = signature
    ex["docstring"] = docstring
    ex["instruction"] = f"Write a Java function `{signature}` to solve the following problem:\n{docstring}"

    return ex

def javascript_instruct(ex):
    """
    Prompt example:
    /* Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    >>> hasCloseElements([1.0, 2.0, 3.0], 0.5)
    false
    >>> hasCloseElements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    true
    */
    const hasCloseElements = (numbers, threshold) => {
    """
    prompt = ex["prompt"]

    lines = [line.strip() for line in prompt.split("\n") if line.strip()]
    function = lines[-1]
    signature = function.strip("{").strip().strip("=>").strip()
    splits = re.split("(\/\*|\*\/)", prompt)

    # Before \*, \*, in-between, \*, after \*
    assert len(splits) >= 5, f"Error in splitting function declaration. Prompt: {prompt} Splits: {str(splits)}"    

    left, middle, _ = splits[-5], splits[-3], splits[-1]

    docstring = "\n".join([x.strip() for x in middle.split("\n") if x.strip()])

    ex["signature"] = signature
    ex["docstring"] = docstring
    ex["instruction"] = f"Write a JavaScript function `{signature}` to solve the following problem:\n{docstring}"

    return ex


def go_instruct(ex):
    """
    Prompt example:
    import (
        "math"
    )

    // Check if in given list of numbers, are any two numbers closer to each other than given threshold.
    // >>> HasCloseElements([]float64{1.0, 2.0, 3.0}, 0.5)
    // false
    // >>> HasCloseElements([]float64{1.0, 2.8, 3.0, 4.0, 5.0, 2.0}, 0.3)
    // true
    func HasCloseElements(numbers []float64, threshold float64) bool {
    """
    prompt = ex["prompt"]

    lines = [line.strip() for line in prompt.split("\n") if line.strip()]
    function = lines[-1]
    signature = function.strip("{").strip()
    is_comment = False
    comment_lines = []
    for line in reversed(lines):
        if line.strip().startswith("//"):
            is_comment = True
            comment_lines.append(line.strip("//").strip())
        # New comment that is not part of the function
        elif is_comment:
            break
    docstring = "\n".join([x.strip() for x in reversed(comment_lines) if x.strip()])

    ex["signature"] = signature
    ex["docstring"] = docstring
    ex["instruction"] = f"Write a Go function `{signature}` to solve the following problem:\n{docstring}"

    return ex

def rust_instruct(ex):
    """
    Prompt example:
    
    /*
    Check if in given list of numbers, are any two numbers closer to each other than
        given threshold.
        
    */
    Declaration example:

    use std::{slice::Iter, cmp::{max, self}, mem::replace, collections::{HashSet, HashMap}, ops::Index, ascii::AsciiExt};
    use rand::Rng;
    use regex::Regex;
    use md5;
    use std::any::{Any, TypeId};

    fn has_close_elements(numbers:Vec<f32>, threshold: f32) -> bool{    
    """
    prompt = ex["prompt"]
    declaration = ex["declaration"]

    ex["signature"] = declaration.split("fn ")[-1].split("{")[0].strip()
    docstring = []
    for line in prompt.split("\n"):
        if line.strip().startswith("/*"):
            line = line.strip("/*")
        elif line.strip().startswith("*/"):
            line = line.strip("*/")
        line = line.strip()
        if line == '"': continue
        if line:
            docstring.append(line)
    ex["docstring"] = "\n".join(docstring)
    ex["instruction"] = f"Write a Rust function `{ex['signature']}` to solve the following problem:\n{ex['docstring']}"

    return ex

