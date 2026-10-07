class Helper:
    @staticmethod
    def clamp(val:float, low:float, high:float):
        return max(low, min(val, high))

    @staticmethod
    def remap(val:float, min1:float, max1:float, min2:float, max2:float):
        return min2 + (float(val - min1) / float(max1 - min1) * (max2 - min2))