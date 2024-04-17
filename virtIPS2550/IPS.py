# %%
# version 1.0

import numpy as np
from dataclasses import dataclass

GAIN_FACTORS = np.array([
    [0x00, 2.00], [0x01, 2.10], [0x02, 2.18], [0x03, 2.29], [0x04, 2.38], [0x05, 2.50], [0x06, 2.59], [0x07, 2.72],
    [0x08, 2.83], [0x09, 2.97], [0x0A, 3.09], [0x0B, 3.24], [0x0C, 3.36], [0x0D, 3.53], [0x0E, 3.67], [0x0F, 3.85],
    [0x10, 4.00], [0x11, 4.20], [0x12, 4.36], [0x13, 4.58], [0x14, 4.76], [0x15, 4.99], [0x16, 5.19], [0x17, 5.45],
    [0x18, 5.66], [0x19, 5.94], [0x1A, 6.17], [0x1B, 6.48], [0x1C, 6.73], [0x1D, 7.06], [0x1E, 7.34], [0x1F, 7.70],
    [0x20, 8.00], [0x21, 8.40], [0x22, 8.72], [0x23, 9.16], [0x24, 9.51], [0x25, 9.99], [0x26, 10.38], [0x27, 10.89],
    [0x28, 11.31], [0x29, 11.88], [0x2A, 12.34], [0x2B, 12.96], [0x2C, 13.46], [0x2D, 14.13], [0x2E, 14.67], [0x2F, 15.41],
    [0x30, 16.00], [0x31, 16.80], [0x32, 17.45], [0x33, 18.32], [0x34, 19.02], [0x35, 19.98], [0x36, 20.75], [0x37, 21.79],
    [0x38, 22.62], [0x39, 23.76], [0x3A, 24.68], [0x3B, 25.91], [0x3C, 26.91], [0x3D, 28.26], [0x3E, 29.34], [0x3F, 30.81],
    [0x40, 32.00], [0x41, 33.60], [0x42, 34.90], [0x43, 36.64], [0x44, 38.05], [0x45, 39.95], [0x46, 41.50], [0x47, 43.58],
    [0x48, 45.25], [0x49, 47.51], [0x4A, 49.36], [0x4B, 51.83], [0x4C, 53.82], [0x4D, 56.52], [0x4E, 58.69], [0x4F, 61.62],
    [0x50, 64.00], [0x51, 67.20], [0x52, 69.79], [0x53, 73.28], [0x54, 76.10], [0x55, 79.90], [0x56, 83.01], [0x57, 87.16],
    [0x58, 90.50], [0x59, 95.02], [0x5A, 98.72], [0x5B, 103.66], [0x5C, 107.65], [0x5D, 113.03], [0x5E, 117.38], [0x5F, 123.24]
])

@dataclass
class IPS:
    """Class for the IPS sensor"""
    gain_boost: bool = False
    gain_code: int = 95
    fine_gain_1_code: float = 0
    fine_gain_2_code: float = 0
    r1_offset_code: float = 0
    r2_offset_code: float = 0
    vlc: float = 2.5
    
    def fine_gain(self, code) -> float:
        return 1.0 + code * 0.125/100.0 * 2.0
    
    def offset(self, code) -> float:
        return code * 4 * 0.0015/100.0 * self.vlc
    
    @property
    def global_gain(self) -> float:
        boost = 2.0 if self.gain_boost else 1.0
        return GAIN_FACTORS[self.gain_code][1] * boost
    
    @property
    def gain_1(self) -> float:
        return self.fine_gain(self.fine_gain_1_code) * self.global_gain
    
    @property
    def gain_2(self) -> float:
        return self.fine_gain(self.fine_gain_2_code) * self.global_gain
    
    @property
    def offset1(self):
        return self.offset(self.r1_offset_code)
    
    @property
    def offset2(self):
        return self.offset(self.r2_offset_code)

    def measurement1(self, voltage):
        return (voltage + self.offset1) * self.gain_1 
    
    def measurement2(self, voltage):
        return (voltage + self.offset2) * self.gain_2

if __name__ == "__main__":
    pass