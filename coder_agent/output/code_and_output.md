```python
def findMedianSortedArrays(nums1, nums2):
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    x, y = len(nums1), len(nums2)
    low, high = 0, x

    while low <= high:
        partitionX = (low + high) // 2
        partitionY = (x + y + 1) // 2 - partitionX

        # If partitionX is 0 it means nothing is there on left side. Use -inf for maxLeftX
        # If partitionX is length of input then there is nothing on right side. Use +inf for minRightX
        maxLeftX = float('-inf') if partitionX == 0 else nums1[partitionX - 1]
        minRightX = float('inf') if partitionX == x else nums1[partitionX]

        maxLeftY = float('-inf') if partitionY == 0 else nums2[partitionY - 1]
        minRightY = float('inf') if partitionY == y else nums2[partitionY]

        if maxLeftX <= minRightY and maxLeftY <= minRightX:
            # We have partitioned array at the correct place
            if (x + y) % 2 == 0:
                return (max(maxLeftX, maxLeftY) + min(minRightX, minRightY)) / 2
            else:
                return max(maxLeftX, maxLeftY)
        elif maxLeftX > minRightY:
            # We are too far on right side for partitionX. Go on left side.
            high = partitionX - 1
        else:
            # We are too far on left side for partitionX. Go on right side.
            low = partitionX + 1

# Example usage:
nums1_example1 = [1, 3]
nums2_example1 = [2]
median_example1 = findMedianSortedArrays(nums1_example1, nums2_example1)

nums1_example2 = [1, 2]
nums2_example2 = [3, 4]
median_example2 = findMedianSortedArrays(nums1_example2, nums2_example2)

median_example1, median_example2
```

Output:
- For the input arrays `nums1 = [1,3]` and `nums2 = [2]`, the median is `2.00000`.
- For the input arrays `nums1 = [1,2]` and `nums2 = [3,4]`, the median is `2.50000`.