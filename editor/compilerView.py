import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from compilers.settings import BASE_DIR
import subprocess
import os
import tempfile
import uuid


# python3 g++ gcc javascript golang ruby 

def run_code(code, language, stdin=""):
    # Create a temporary directory to store files
    print(stdin)
    with tempfile.TemporaryDirectory() as temp_dir:
        if language == "python":
            try:
                # Generate a random file name for the Python code
                code_file_name = str(uuid.uuid4()) + '.py'
                code_file = os.path.join(temp_dir, code_file_name)
                with open(code_file, 'w') as file:
                    file.write(code)

                # Execute the Python code using subprocess with stdin
                result = subprocess.run(
                    ["python3", code_file],  # Use "python" to invoke the Python interpreter
                    input=stdin,  # Pass stdin as a string
                    capture_output=True,
                    text=True,
                    encoding="utf-8",  # Specify the encoding
                )
                # Get the output and error (if any)
                output = result.stdout
                error = result.stderr

                if error:
                    return JsonResponse({"error": error})
                else:
                    return JsonResponse({"output": output})

            except Exception as e:
                return JsonResponse({"error": str(e)})

        elif language == "c" or language == "cpp": 
            compiler_name = "g++" if language == "cpp" else "gcc"
            
            
            # Check if the compiler executable exists
    
    
            try:
                # Generate random file names for the source code and executable
                source_file_name = str(uuid.uuid4()) + ('.cpp' if language == "cpp" else '.c')
                source_file = os.path.join(temp_dir, source_file_name)

                # Write the code to the source file
                with open(source_file, 'w') as file:
                    file.write(code)

                # Generate a random name for the executable
                executable_file_name = str(uuid.uuid4()) + '.out'
                executable_file = os.path.join(temp_dir, executable_file_name)

                # Compile the C/C++ code using subprocess
                compile_command = [compiler_name, source_file, '-o', executable_file]
                compile_result = subprocess.run(
                    compile_command, capture_output=True, text=True, input=stdin  # Removed encoding parameter
                )

                if compile_result.returncode == 0:
                    # Compilation was successful, now run the executable with stdin
                    execution_result = subprocess.run(
                        [executable_file],
                        capture_output=True,
                        text=True,
                        input=stdin  # Removed encoding parameter
                    )
                    output = execution_result.stdout
                    error = execution_result.stderr

                    if error:
                        return JsonResponse({"error": error})
                    else:
                        return JsonResponse({"output": output})
                else:
                    # Compilation failed
                    error = compile_result.stderr
                    return JsonResponse({"error": error})

            except Exception as e:
                return JsonResponse({"error": str(e)})

        elif language == "javascript":
            nodejs_interpreter_path = os.path.join(BASE_DIR, 'compiler', 'node', 'bin', 'node')

        # Check if the Node.js interpreter executable exists
            if not os.path.exists(nodejs_interpreter_path):
                return JsonResponse({"error": "Node.js interpreter not found."})

            try:
            # Generate a random file name for the Node.js code
                code_file_name = str(uuid.uuid4()) + '.js'
                code_file = os.path.join(temp_dir, code_file_name)
                with open(code_file, 'w') as file:
                    file.write(code)

                # Execute the Node.js code using subprocess with stdin
                result = subprocess.run(
                    [nodejs_interpreter_path, code_file],
                    capture_output=True,
                    text=True,
                    input=stdin  # Use a Unicode string for input
                )

                # Get the output and error (if any)
                output = result.stdout
                error = result.stderr

                if error:
                    return JsonResponse({"error": error})
                else:
                    return JsonResponse({"output": output})

            except Exception as e:
                return JsonResponse({"error": str(e)})

        
        elif language == "go":
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    # Generate a random file name for the Go code
                    code_file_name = str(uuid.uuid4()) + '.go'
                    code_file = os.path.join(temp_dir, code_file_name)
                    with open(code_file, 'w') as file:
                        file.write(code)

                    # Define the path to the Go compiler (go.exe)
                    
                    
                    # Check if the Go compiler executable exists
                    

                    # Compile and run the Go code using subprocess with stdin
                    compile_command = ["go", 'run', code_file]
                    compile_result = subprocess.run(
                        compile_command, capture_output=True, text=True, input=stdin
                    )

                    if compile_result.returncode == 0:
                        # Compilation and execution were successful
                        output = compile_result.stdout
                        error = compile_result.stderr

                        if error:
                            return JsonResponse({"error": error})
                        else:
                            return JsonResponse({"output": output})
                    else:
                        # Compilation failed
                        error = compile_result.stderr
                        return JsonResponse({"error": error})

                except Exception as e:
                    return JsonResponse({"error": str(e)})
        
        
        elif language == "ruby":
            with tempfile.TemporaryDirectory() as temp_dir:
                try:
                    # Generate a random file name for the Ruby code
                    code_file_name = str(uuid.uuid4()) + '.ruby'
                    code_file = os.path.join(temp_dir, code_file_name)
                    with open(code_file, 'w') as file:
                        file.write(code)


                    

                    # Compile and run the Go code using subprocess with stdin
                    compile_command = ["ruby", code_file]

                    compile_result = subprocess.run(
                        compile_command, capture_output=True, text=True, input=stdin
                    )

                    if compile_result.returncode == 0:
                        # Compilation and execution were successful
                        output = compile_result.stdout
                        error = compile_result.stderr

                        if error:
                            return JsonResponse({"error": error})
                        else:
                            return JsonResponse({"output": output})
                    else:
                        # Compilation failed
                        error = compile_result.stderr
                        return JsonResponse({"error": error})

                except Exception as e:
                    return JsonResponse({"error": str(e)})
        
        
        elif language == "java":
            try:
                # Generate a random file name for the Java code
                code_file_name = str(uuid.uuid4()) + '.java'
                code_file = os.path.join(temp_dir, code_file_name)
                with open(code_file, 'w') as file:
                    file.write(code)

                # Compile the Java code using subprocess
                compile_command = ["javac", code_file]
                compile_result = subprocess.run(
                    compile_command, capture_output=True, text=True
                )

                if compile_result.returncode == 0:
                    # Compilation was successful, now run the Java program
                    class_name = code_file_name.replace(".java", "")
                    run_command = ["java", class_name]
                    run_result = subprocess.run(
                        run_command,
                        capture_output=True,
                        text=True,
                        input=stdin
                    )
                    output = run_result.stdout
                    error = run_result.stderr

                    if error:
                        return JsonResponse({"error": error})
                    else:
                        return JsonResponse({"output": output})
                else:
                    # Compilation failed
                    error = compile_result.stderr
                    return JsonResponse({"error": error})

            except Exception as e:
                return JsonResponse({"error": str(e)})

        else:
            return JsonResponse({"error": f"Language {language} is not supported."})




@csrf_exempt
def compiler(request):
    if request.method == "POST":
        try:
            # Parse the JSON data sent in the request body
            data = json.loads(request.body.decode("utf-8"))
            code = data.get("code", "")  # Get the "code" field from the JSON data
            language = data.get("language", "")
            stdin = data.get("stdin", "")  # Get the "stdin" field from the JSON data
            result = run_code(code, language, stdin)
            return result
        except json.JSONDecodeError as e:
            # Handle JSON decoding error
            return JsonResponse({"error": "JSON decoding error"})
    return HttpResponse("Method not allowed", status=405)
