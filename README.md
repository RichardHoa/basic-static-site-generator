# Static Site Generator Project

This project is a basic static site generator created with the help of Bootdev. It converts markdown (`.md`) files into HTML pages, allowing you to create a simple, static website quickly and easily.

## How to Use This Project

1. **Add Markdown Files**: 
   - Place your markdown files (`.md`) in the `content` directory.
   - Each new URL page should be placed in a new directory within the `content` folder.

2. **Run the Generator**:
   - In the root folder of the project, run the following command:
     ```bash
     ./main.sh
     ```
   - This command will start a local server on port 8888, hosting all the generated HTML files.

3. **Access Your Site**:
   - Open your web browser and navigate to `http://localhost:8888` to view your beautiful HTML pages!

The static site generator reads the markdown files from the `content` directory, processes them, and outputs corresponding HTML files that are ready to be served.

