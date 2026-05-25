# app/services/professional_scanner.py
# WORLD-CLASS MEDICAL DOCUMENT SCANNER
# Scans reports, prescriptions, lab results - produces 100% clean digital copies

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import os
import uuid
from datetime import datetime

class ProfessionalScanner:
    def __init__(self):
        self.output_dir = "uploads/reports"
        os.makedirs(f"{self.output_dir}/original", exist_ok=True)
        os.makedirs(f"{self.output_dir}/scanned", exist_ok=True)
        os.makedirs(f"{self.output_dir}/enhanced", exist_ok=True)
    
    def scan_document(self, image_path, document_type="report"):
        """
        Complete document scanning pipeline
        Returns: paths to all versions + extracted data
        """
        result = {
            "success": False,
            "original_path": image_path,
            "scanned_path": "",
            "enhanced_path": "",
            "pdf_path": "",
            "document_type": document_type,
            "quality_score": 0,
        }
        
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                result["error"] = "Cannot read image file"
                return result
            
            original_height, original_width = image.shape[:2]
            
            # Step 1: Detect document edges and crop
            warped = self.detect_and_crop_document(image)
            
            # Step 2: Enhance for perfect readability
            enhanced = self.enhance_document(warped)
            
            # Step 3: Remove shadows and fix lighting
            cleaned = self.remove_shadows(enhanced)
            
            # Step 4: Sharpen text
            sharpened = self.sharpen_text(cleaned)
            
            # Step 5: Final polish
            final = self.final_polish(sharpened)
            
            # Generate unique filename
            doc_id = str(uuid.uuid4())[:8]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = f"scan_{document_type}_{timestamp}_{doc_id}"
            
            # Save all versions
            scanned_path = f"{self.output_dir}/scanned/{base_name}_scanned.jpg"
            enhanced_path = f"{self.output_dir}/enhanced/{base_name}_enhanced.jpg"
            
            cv2.imwrite(scanned_path, final)
            
            # Create ultra-enhanced version for readability
            ultra = self.ultra_enhance(final)
            cv2.imwrite(enhanced_path, ultra)
            
            # Calculate quality score
            quality = self.assess_quality(final, original_height, original_width)
            
            result.update({
                "success": True,
                "scanned_path": scanned_path,
                "enhanced_path": enhanced_path,
                "quality_score": quality,
                "original_size": f"{original_width}x{original_height}",
                "final_size": f"{final.shape[1]}x{final.shape[0]}",
            })
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def detect_and_crop_document(self, image):
        """Detect document edges and apply perspective correction"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edged = cv2.Canny(blurred, 50, 150)
        
        # Dilate edges to close gaps
        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(edged, kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return image
        
        # Find the largest contour (should be the document)
        largest = max(contours, key=cv2.contourArea)
        
        # Get the 4 corners
        peri = cv2.arcLength(largest, True)
        approx = cv2.approxPolyDP(largest, 0.02 * peri, True)
        
        if len(approx) == 4:
            # Apply perspective transform
            warped = self.four_point_transform(image, approx.reshape(4, 2))
            return warped
        
        # If no clear 4 corners, use the bounding rectangle
        x, y, w, h = cv2.boundingRect(largest)
        return image[y:y+h, x:x+w]
    
    def four_point_transform(self, image, pts):
        """Apply perspective correction"""
        # Order points: top-left, top-right, bottom-right, bottom-left
        rect = self.order_points(pts)
        (tl, tr, br, bl) = rect
        
        # Calculate width
        width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        max_width = max(int(width_a), int(width_b))
        
        # Calculate height
        height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        max_height = max(int(height_a), int(height_b))
        
        # Destination points
        dst = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]
        ], dtype="float32")
        
        # Transform
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (max_width, max_height))
        
        return warped
    
    def order_points(self, pts):
        """Order corner points"""
        rect = np.zeros((4, 2), dtype="float32")
        
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]  # top-left
        rect[2] = pts[np.argmax(s)]  # bottom-right
        
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]  # top-right
        rect[3] = pts[np.argmax(diff)]  # bottom-left
        
        return rect
    
    def enhance_document(self, image):
        """Enhance document for perfect readability"""
        # Convert to PIL for enhancement
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # Increase contrast
        enhancer = ImageEnhance.Contrast(pil_image)
        pil_image = enhancer.enhance(1.8)
        
        # Increase sharpness
        enhancer = ImageEnhance.Sharpness(pil_image)
        pil_image = enhancer.enhance(2.0)
        
        # Increase brightness slightly
        enhancer = ImageEnhance.Brightness(pil_image)
        pil_image = enhancer.enhance(1.1)
        
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    def remove_shadows(self, image):
        """Remove shadows and normalize lighting"""
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge back
        lab = cv2.merge([l, a, b])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    def sharpen_text(self, image):
        """Sharpen text for crystal clear reading"""
        # Create sharpening kernel
        kernel = np.array([
            [-1, -1, -1],
            [-1, 9, -1],
            [-1, -1, -1]
        ])
        
        return cv2.filter2D(image, -1, kernel)
    
    def final_polish(self, image):
        """Final polish - convert to clean black & white document"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Adaptive threshold for clean B&W
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Remove small noise
        kernel = np.ones((2, 2), np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        # Add slight border for professional look
        bordered = cv2.copyMakeBorder(cleaned, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)
        
        return cv2.cvtColor(bordered, cv2.COLOR_GRAY2BGR)
    
    def ultra_enhance(self, image):
        """Create ultra-high-quality version for printing"""
        # Upscale if needed (maintain aspect ratio)
        h, w = image.shape[:2]
        if w < 1200:
            scale = 1200 / w
            new_w = 1200
            new_h = int(h * scale)
            image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
        
        # Apply final enhancements
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        enhancer = ImageEnhance.Contrast(pil_image)
        pil_image = enhancer.enhance(1.3)
        enhancer = ImageEnhance.Sharpness(pil_image)
        pil_image = enhancer.enhance(1.5)
        
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    def assess_quality(self, image, orig_h, orig_w):
        """Assess scan quality score (0-100)"""
        score = 0
        
        # Size maintained
        h, w = image.shape[:2]
        size_ratio = min(w/orig_w, h/orig_h)
        if size_ratio > 0.5:
            score += 30
        else:
            score += 15
        
        # Contrast check
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        std = np.std(gray)
        if std > 50:
            score += 35
        elif std > 30:
            score += 20
        else:
            score += 10
        
        # Edge sharpness
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (h * w)
        if edge_density > 0.05:
            score += 35
        elif edge_density > 0.02:
            score += 20
        else:
            score += 10
        
        return min(100, score)

# Create singleton instance
scanner = ProfessionalScanner()