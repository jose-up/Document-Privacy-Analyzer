class PDFUploadChecker {
    constructor() {
        this.uploadArea = document.getElementById('uploadArea');
        this.fileInput = document.getElementById('fileInput');
        this.result = document.getElementById('result');
        this.fileInfo = document.getElementById('fileInfo');
        this.clearBtn = document.getElementById('clearBtn');
        
        this.init();
    }
    
    init() {
        // Click to upload
        this.uploadArea.addEventListener('click', () => {
            this.fileInput.click();
        });
        
        // File selection
        this.fileInput.addEventListener('change', (e) => {
            this.handleFile(e.target.files[0]);
        });
        
        // Drag and drop
        this.uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadArea.classList.add('dragover');
        });
        
        this.uploadArea.addEventListener('dragleave', () => {
            this.uploadArea.classList.remove('dragover');
        });
        
        this.uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadArea.classList.remove('dragover');
            this.handleFile(e.dataTransfer.files[0]);
        });
        
        // Clear button
        this.clearBtn.addEventListener('click', () => {
            this.reset();
        });
    }
    
    handleFile(file) {
        if (!file) {
            this.showError('No file selected');
            return;
        }
        
        // Check if it's a PDF
        const isPDF = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf');
        
        if (isPDF) {
            this.showSuccess('✓ Valid PDF file uploaded!');
            this.displayFileInfo(file);
        } else {
            this.showError('✗ Invalid file type. Please upload a PDF file.');
            this.hideFileInfo();
        }
    }
    
    showSuccess(message) {
        this.result.className = 'result success';
        this.result.textContent = message;
        this.clearBtn.style.display = 'block';
    }
    
    showError(message) {
        this.result.className = 'result error';
        this.result.textContent = message;
        this.clearBtn.style.display = 'block';
    }
    
    displayFileInfo(file) {
        document.getElementById('fileName').textContent = file.name;
        document.getElementById('fileSize').textContent = this.formatFileSize(file.size);
        document.getElementById('fileType').textContent = file.type || 'application/pdf';
        document.getElementById('fileDate').textContent = new Date(file.lastModified).toLocaleString();
        this.fileInfo.style.display = 'block';
    }
    
    hideFileInfo() {
        this.fileInfo.style.display = 'none';
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }
    
    reset() {
        this.fileInput.value = '';
        this.result.style.display = 'none';
        this.hideFileInfo();
        this.clearBtn.style.display = 'none';
    }
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    new PDFUploadChecker();
});
