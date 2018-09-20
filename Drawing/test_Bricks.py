import numpy as np
import GCode

# Standard brick dimensions.
BrickHeight = 65  # [mm]
BrickLength = 225  # [mm]
BrickDepth = 12.5  # [mm]
# Yes, I realize the error, but too many patterns made...
BrickRatio = 215 / 65  # [dimensionless]

# Poplar 1x4". Cut
BlockHeight = 89.0  # [mm]
BlockLength = 2 * BlockHeight  # [mm]

# Drawing configuration.
# How many rows of bricks to draw on the block.
N_BrickRows = 12  # [dimensionless]

# Dimensions of a 'brick' projected onto the block of wood.
H_Block_Brick = BlockHeight / N_BrickRows  # [mm]
L_Block_Brick = H_Block_Brick * BrickRatio  # [mm]

flip = np.array([[1, 1], [1, 0]])
transform_tuple = (
    np.eye(2),  # Identity matrix, do nothing.
    flip,  # Flip the matrix, reduces travel time.
)
vertical_brick_lines_tuple = (
    np.arange(L_Block_Brick, BlockLength, L_Block_Brick),  # Odd rows.
    np.arange(L_Block_Brick / 2, BlockLength, L_Block_Brick),  # Even rows.
)
horizontal_brick_lines = np.linspace(
    0, BlockHeight, N_BrickRows, endpoint=False
)

BlockBrick = GCode.Program()
BlockBrick.lines = list()

for idx in range(1, len(horizontal_brick_lines)):
    # Top horizontal line that defines each 'brick'
    horizontal_brick_line = horizontal_brick_lines[idx]
    row_line_points = np.array(
        [[0, horizontal_brick_line], [BlockLength, horizontal_brick_line]]
    )
    # Transform to perform on the row points.
    transform = transform_tuple[np.mod(idx, 2)]

    row_line_points = np.matmul(transform, row_line_points)
    line_ = GCode.Line(points=row_line_points)

    BlockBrick.lines.append(line_)

assert N_BrickRows - len(BlockBrick.lines) == 1, "Something's Broken"
assert np.isclose(BlockBrick.dist, 2416.0212033333337), "Something's Broken"
