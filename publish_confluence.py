print("Python script is running")

#with open("wiki/Home.md", "r") as file: means: open the Home.md file inside the wiki folder in read mode. "r" means read.

with open("wiki/Home.md", "r") as file:  
  content = file.read()                 #reads everything inside Home.md and stores it in content.

print("Wiki Home page content:")
print(content)
