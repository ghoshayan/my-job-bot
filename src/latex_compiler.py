import yaml
import jinja2
import os
import subprocess

def compile_dynamic_resume(yaml_path, template_path, output_tex_path, output_dir):
    # 1. Load the candidate data
    with open(yaml_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    # 2. Configure Jinja2 to NOT conflict with LaTeX {}
    latex_jinja_env = jinja2.Environment(
        block_start_string='\\BLOCK{',
        block_end_string='}',
        variable_start_string='\\VAR{',
        variable_end_string='}',
        comment_start_string='\\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.dirname(template_path))
    )

    # 3. Render the template with YAML data
    template_name = os.path.basename(template_path)
    template = latex_jinja_env.get_template(template_name)
    rendered_tex = template.render(**data)

    # 4. Save the dynamically generated .tex file
    with open(output_tex_path, 'w', encoding='utf-8') as f:
        f.write(rendered_tex)
    
    print(f"Successfully generated custom LaTeX file: {output_tex_path}")

    # 5. Compile to PDF (Requires pdflatex installed on your host machine)
    try:
        print("Compiling PDF...")
        subprocess.run(
            ['pdflatex', '-interaction=batchmode', f'-output-directory={output_dir}', output_tex_path],
            check=True
        )
        print("PDF Compilation complete!")
    except FileNotFoundError:
        print("Warning: 'pdflatex' command not found. The .tex file was generated, but to compile it into a PDF locally, you need to install a TeX distribution (like MiKTeX or TeX Live).")
    except subprocess.CalledProcessError as e:
        print(f"LaTeX compilation failed with error: {e}")

if __name__ == "__main__":
    # Ensure this runs from the root directory 'my-job-bot'
    compile_dynamic_resume(
        yaml_path='master_data.yaml',
        template_path='templates/resume.tex',
        output_tex_path='templates/custom_resume_output.tex',
        output_dir='templates/'
    )