from PIL import Image
import os
import glob

def split_and_rotate_image(input_path, output_dir):
    """
    Split an image in the middle and rotate both halves.
    
    Args:
        input_path (str): Path to the input image
        output_dir (str): Directory to save output images
    
    Returns:
        tuple: Paths to the two output images
    """
    try:
        # Load the image
        img = Image.open(input_path)
        
        # Get image dimensions
        width, height = img.size
        
        # Calculate middle point
        mid_x = width // 2
        
        # Split the image into left and right halves
        left_half = img.crop((0, 0, mid_x, height))
        right_half = img.crop((mid_x, 0, width, height))
        
        # Rotate both halves (90 degrees clockwise for the first half, 
        # 90 degrees counterclockwise for the second half)
        left_half_rotated = left_half.rotate(-90, expand=True)
        right_half_rotated = right_half.rotate(90, expand=True)
        
        # Create output filenames
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        left_output = os.path.join(output_dir, f"{base_name}_left_rotated.jpg")
        right_output = os.path.join(output_dir, f"{base_name}_right_rotated.jpg")
        
        # Save the rotated images
        left_half_rotated.save(left_output)
        right_half_rotated.save(right_output)
        
        print(f"Processed: {os.path.basename(input_path)}")
        return left_output, right_output
    
    except Exception as e:
        print(f"Error processing {os.path.basename(input_path)}: {e}")
        return None

def process_folder(input_folder, output_folder=None):
    """
    Process all images in a folder.
    
    Args:
        input_folder (str): Path to the folder containing images
        output_folder (str, optional): Directory to save output images. If None, creates 'output' subfolder
    """
    # Create output directory if it doesn't exist
    if output_folder is None:
        output_folder = os.path.join(input_folder, "output")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output directory: {output_folder}")
    
    # Get all image files in the folder
    image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif", "*.tiff"]
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_folder, ext)))
        image_files.extend(glob.glob(os.path.join(input_folder, ext.upper())))
    
    if not image_files:
        print(f"No image files found in {input_folder}")
        return
    
    print(f"Found {len(image_files)} images to process...")
    
    # Process each image
    for img_path in image_files:
        split_and_rotate_image(img_path, output_folder)
    
    print(f"Processing complete. Results saved to {output_folder}")

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2] if len(sys.argv) > 2 else None
        process_folder(input_folder, output_folder)
    else:
        print("Usage: python script.py input_folder [output_folder]")
        print("       If output_folder is not specified, images will be saved to an 'output' subfolder")