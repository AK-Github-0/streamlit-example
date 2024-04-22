import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import requests
import time
import random
import os

gl_background_size = (1024, 1024)

gl_image = Image.new("RGB", gl_background_size, "black")

class BackgroundGenerator:
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        self.headers = {"Authorization": "Bearer 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"}
        self.genre_options = ["Event", "Educational", "Health"]

    def query(self, payload):
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.content

    def generate_background(self, genre, prompt):
        seed = random.randint(0,10000)
        payload = {"inputs": f"{prompt} for the background of poster of {genre} genre , ((no text))", "seed": seed,"negative_prompt":"(text)"}
        return self.query(payload)

    def regenerate_background(self, genre, feedback, prompt):
        seed = random.randint(0,10000)
        payload = {"inputs": f"{prompt} and {feedback} for the background of poster of {genre} genre ,((no text))", "seed": seed,"negative_prompt":"(text)"}
        return self.query(payload)

    def run(self):
        st.title("Automated Poster Generation and Customization")

        selected_genre = st.selectbox("Select a genre:", self.genre_options)
        subgenres = {
            'Event': ["Concert", "Festival", "Movie", "Sports","User Specific"],
            'Educational': ["Science Fair", "Academic Conference", "Educational Workshop"],
            'Health': ["Health Awareness", "Medical Conference", "Vaccination Campaign"]
        }
        selected_subgenre = st.selectbox(f"Select a subgenre of {selected_genre}:", subgenres[selected_genre])

        prompts_dict = {
    "User Specific":"Design a bright, simple, single or two colours backgorund for a poster with no text:0.3",
    "Concert": "Design a vibrant concert poster backgorund capturing the essence of the indie music scene. Incorporate a dynamic blend of colors and imagery that resonates with the indie vibe. Include silhouettes or stylized representations of people immersed in the concert experience, conveying the energy and excitement of live music with no text:0.3",
    "Festival": "Generate a vibrant festival poster. Blend a kaleidoscope of colors seamlessly, incorporating elements like confetti, candles and other festive props. Capture the lively spirit of the event with dynamic compositions and energetic visuals with no text:0.3",
    "Sports": "Design a dynamic sports poster featuring a striking silhouette of a determined runner against a vibrant background, capturing the essence of speed and endurance. Incorporate bold typography to highlight the event details and use energetic colors to evoke a sense of excitement.",
    "Movie": "Generate an image for a movie poster with a suspicious theme. Use a darker color scheme to create an atmosphere of intrigue and uncertainty. Depict abstract elements that hint at secrecy, such as obscured silhouettes, hidden symbols, or veiled objects. Utilize shades of mysterious grays, and subtle hints of intense color to convey a sense of suspense. Ensure the overall composition sparks curiosity and invites viewers to delve into the enigma behind the movie with no text:0.3",
    "Science Fair": "Generate an eye-catching science fair poster featuring a captivating depiction of nucleus, microscopes, and a beaker with vividly colored chemicals. Explore the hidden world of atoms and molecules, showcasing the beauty and complexity of the microcosm through striking visuals with no text:0.3",
    "Educational Workshop": "Generate an image depicting a dynamic educational workshop scenario, featuring a business professional engaged in interactive learning with state-of-the-art technology. Emphasize collaboration, innovation, and the integration of cutting-edge tools within the educational environment with no text:0.3",
    "Health Awareness": "Generate a health awareness background featuring a prominent illustration.Include relevant props such as pills, a balanced diet, and exercise imagery. Emphasize vibrant colors and use persuasive text to convey the importance of a healthy lifestyle for overall well-being with no text:0.3",
    "Medical Conference": "Create a captivating medical conference background featuring a prominent display of a DNA helix or a vibrant cell pattern seamlessly integrated across the poster. Emphasize a professional and visually appealing composition to enhance the overall visual impact and convey the theme of cutting-edge advancements in medical research and innovation with no text:0.3",
    "Vaccination Campaign": "Capture the joy of a healthy childhood! Design a vibrant vaccination awareness poster featuring playful silhouettes of children laughing and playing, harmoniously juxtaposed with the caring image of a doctor holding a vaccination injection. Encourage community health through the power of preventive care with no text:0.3",
    "Academic Conference" : "Explore the fusion of cutting-edge technology and academic poster presentation by designing a visually engaging poster that incorporates an LCD screen. Showcase the latest advancements in your field using dynamic symbols and interactive elements on the screen, creating an immersive experience for conference attendees. Highlight how this innovative format enhances the dissemination of research findings and facilitates a deeper understanding of complex concepts with no text:0.4"
}

        original_prompt = prompts_dict[selected_subgenre]
        prompt = original_prompt
        # background_size = (1024, 1024)
        # image = Image.new("RGB", background_size, "black")
        if st.button("Generate Poster Background"):
            st.text("Generating Poster Background...")
            image_bytes = self.generate_background(selected_genre, prompt)
            try:
                image = Image.open(io.BytesIO(image_bytes))
                file_path = 'saved_image.jpg'
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"The file {file_path} has been deleted successfully.")
                else:
                    print(f"The file {file_path} does not exist.")
                image.save('saved_image.jpg')
            except:
                image_bytes = self.generate_background(selected_genre, prompt)
                image = Image.open(io.BytesIO(image_bytes))
                file_path = 'saved_image.jpg'
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"The file {file_path} has been deleted successfully.")
                else:
                    print(f"The file {file_path} does not exist.")
                image.save('saved_image.jpg')


        if st.button("Regenerate Poster Background"):
            feedback = st.text_input("Please write feedback for the background:")
            st.text("Regenerating Poster Background...")
            time.sleep(10)
            image_bytes = self.regenerate_background(selected_genre, feedback, prompt)
            image = Image.open(io.BytesIO(image_bytes))
            file_path = 'saved_image.jpg'
            # Check if the file exists and then delete it
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"The file {file_path} has been deleted successfully.")
            else:
                print(f"The file {file_path} does not exist.")
            
            image.save('saved_image.jpg')



def resize_with_aspect_ratio(image, width=None, height=None):
    original_width, original_height = image.size

    if width is None and height is None:
        return image

    if width is not None and height is not None:
        raise ValueError("You must specify either width or height, not both.")

    if width is not None:
        aspect_ratio = width / original_width
        new_height = int(original_height * aspect_ratio)
        return image.resize((width, new_height))

    if height is not None:
        aspect_ratio = height / original_height
        new_width = int(original_width * aspect_ratio)
        return image.resize((new_width, height))

def overlay_image(background_image, overlay_image, x, y):
    overlay_image = overlay_image.convert("RGBA")
    background_image.paste(overlay_image, (x, y), overlay_image)
    return background_image

def add_text(background_image, text, position, font_size, font_color, font_style):
    draw = ImageDraw.Draw(background_image)
    font_path = get_font_path(font_style)
    font = ImageFont.truetype(font_path, font_size)

    draw.text(position, text, font=font, fill=font_color)

def get_font_path(font_style):
    if font_style == "Arial":
        return "arial.ttf"
    elif font_style == "Times New Roman":
        return "times.ttf"
    elif font_style == "Courier New":
        return "cour.ttf"
    elif font_style == "Impact":
        return "impact.ttf"  
    elif font_style == "Cooper Black":
        return "cooperblack.ttf"  
    elif font_style == "Lobster":
        return "lobster.ttf"  
    elif font_style == "Pacifico":
        return "pacifico.ttf"  
    elif font_style == "Playbill":
        return "playbill.ttf"  
    elif font_style == "Chiller":
        return "chiller.ttf"

def download_edited_poster(background_image):
        image_bytes = io.BytesIO()
        background_image.save(image_bytes, format='PNG')
        st.download_button(
            label="Download Edited Poster",
            data=image_bytes.getvalue(),
            file_name='edited_poster.png',
            mime='image/png'
        )

if __name__ == "__main__":
    generator = BackgroundGenerator()
    generator.run()
    background_size = (1024, 1024)

#    background_image = Image.new("RGB", background_size, "black")
    background_image = Image.open('saved_image.jpg')

    # st.title("Automated Poster Generation and Customization")

    logo_image = st.sidebar.file_uploader('Upload Logo', type=['jpg', 'jpeg', 'png'])

    if 'logo_x' not in st.session_state:
        st.session_state.logo_x = 0
    if 'logo_y' not in st.session_state:
        st.session_state.logo_y = 0

    if logo_image is not None:
        logo_image = Image.open(logo_image)
        logo_image = logo_image.convert("RGBA")
        logo_width = st.sidebar.slider("Logo Width", 10, background_size[0], 100)

        logo_image = resize_with_aspect_ratio(logo_image, width=logo_width)

        st.sidebar.markdown("### Logo Position")
        st.session_state.logo_x = st.sidebar.slider("Logo X Position", 0, background_size[0] - logo_image.width, st.session_state.logo_x)
        st.session_state.logo_y = st.sidebar.slider("Logo Y Position", 0, background_size[1] - logo_image.height, st.session_state.logo_y)

        background_image = overlay_image(background_image, logo_image, st.session_state.logo_x, st.session_state.logo_y)

    uploaded_images = []
    num_uploaded_images = st.sidebar.number_input("Number of Images to Upload", min_value=1, max_value=10, value=1)

    for i in range(num_uploaded_images):
        uploaded_image = st.sidebar.file_uploader(f'Upload Image {i+1}', type=['jpg', 'jpeg', 'png'])
        if uploaded_image is not None:
            uploaded_images.append(uploaded_image)

    for idx, uploaded_image in enumerate(uploaded_images):
        if uploaded_image is not None:
            image = Image.open(uploaded_image)

            image_width = st.sidebar.slider(f"Image {idx+1} Width", 10, background_size[0], 100)

            image = resize_with_aspect_ratio(image, width=image_width)

            st.sidebar.markdown(f"### Image {idx+1} Position")
            x_position = st.sidebar.slider(f"Image {idx+1} X Position", 0, background_size[0] - image.width, st.session_state.get(f"image_{idx}_x", 0))
            y_position = st.sidebar.slider(f"Image {idx+1} Y Position", 0, background_size[1] - image.height, st.session_state.get(f"image_{idx}_y", 0))

            overlay_image(background_image, image, x_position, y_position)
            
            
            st.session_state[f"image_{idx}_x"] = x_position
            st.session_state[f"image_{idx}_y"] = y_position

    text_controls = st.sidebar.expander("Add Text")

    num_texts = text_controls.number_input("Number of Texts", min_value=1, max_value=10, value=1)

    for i in range(int(num_texts)):
        with st.sidebar.expander(f"Text {i+1}"):
            text = st.text_input(f"Enter Text {i+1}:")
            text_position_x = st.slider(f"Text {i+1} X Position", 0, background_size[0], 0)
            text_position_y = st.slider(f"Text {i+1} Y Position", 0, background_size[1], 0)
            font_size = st.slider(f"Font Size {i+1}", 10, 150, 20)
            font_color = st.color_picker(f"Text Color {i+1}", "#FFFFFF")
            font_style = st.selectbox(f"Font Style {i+1}", ["Arial", "Times New Roman", "Courier New", "Impact"])

            add_text(background_image, text, (text_position_x, text_position_y), font_size, font_color, font_style)

    st.image(background_image, caption='Poster', use_column_width=True)



    download_edited_poster(background_image)


 
