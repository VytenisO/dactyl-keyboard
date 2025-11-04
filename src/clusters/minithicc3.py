from clusters.minidox import MinidoxCluster
import numpy as np

class Minithicc3(MinidoxCluster):
    """
    Minithicc3 thumb cluster - a 3-key thumb cluster variant.

    Key positioning is controlled by:
    - Rotation values in each *_place() function (tl_place, tr_place, ml_place)
    - Translation values in each *_place() function
    - thumb_plate_*_rotation values for individual key rotation

    NOTE: For right-hand cluster, the actual physical layout is:
    - ml = leftmost button
    - tl = middle button
    - tr = rightmost button
    """

    @staticmethod
    def name():
        return "MINITHICC3"

    def __init__(self, parent_locals):
        # Key rotation values (applied after positioning)
        # NOTE: Despite the names, for right-hand cluster:
        # - tr = rightmost key
        # - tl = middle key
        # - ml = leftmost key
        self.thumb_plate_tr_rotation = (0, 0, 0)  # Rightmost key (for right hand)
        self.thumb_plate_tl_rotation = (0, 0, 0)  # Middle key (for right hand)
        self.thumb_plate_ml_rotation = (0, 0, 0)  # Leftmost key (for right hand)

        # Unused rotation variables (kept for compatibility)
        self.thumb_plate_mr_rotation = (0, 0, 0)
        self.thumb_plate_br_rotation = (0, 0, 0)
        self.thumb_plate_bl_rotation = (0, 0, 0)

        self.num_keys = 3
        super().__init__(parent_locals)

        # Import parent locals into global namespace
        for item in parent_locals:
            globals()[item] = parent_locals[item]

    # ============================================================================
    # Key Placement Functions
    # ============================================================================
    # Adjust rotation and translation values here to change thumb cluster angle
    # NOTE: For right-hand cluster - ml=left, tl=middle, tr=right

    def tl_place(self, shape):
        """Position the MIDDLE thumb key (for right hand)."""
        shape = rotate(shape, [14, -50, 20])  # Adjust these values for angle
        shape = translate(shape, [-37, -16, -17])  # Adjust for position
        shape = self.thumb_place(shape)
        return shape

    def tr_place(self, shape):
        """Position the RIGHTMOST thumb key (for right hand)."""
        shape = rotate(shape, [20, -45, 10])  # Adjust these values for angle
        shape = translate(shape, [-21, -10, -6])  # Adjust for position
        shape = self.thumb_place(shape)
        return shape

    def ml_place(self, shape):
        """Position the LEFTMOST thumb key (for right hand)."""
        shape = rotate(shape, [1, -65, 40])  # Adjust these values for angle
        shape = translate(shape, [-46, -22, -32])  # Adjust for position
        shape = self.thumb_place(shape)
        return shape

    # ============================================================================
    # Layout Functions
    # ============================================================================

    def thumb_1x_layout(self, shape, cap=False):
        """Layout for 1x thumb keys (currently unused)."""
        debugprint('thumb_1x_layout()')
        return None

    def thumb_15x_layout(self, shape, cap=False, plate=True):
        """Layout for 1.5x thumb keys."""
        debugprint('thumb_15x_layout()')
        return union([
            self.tr_place(rotate(shape, [0, 0, self.thumb_plate_tr_rotation])),  # Right
            self.tl_place(rotate(shape, [0, 0, self.thumb_plate_tl_rotation])),  # Middle
            self.ml_place(rotate(shape, [0, 0, self.thumb_plate_ml_rotation])),  # Left
        ])

    def thumb_fx_layout(self, shape):
        """Flexible layout for thumb cluster."""
        return union([
            self.tr_place(rotate(shape, [0, 0, self.thumb_plate_tr_rotation])),  # Right
            self.tl_place(rotate(shape, [0, 0, self.thumb_plate_tl_rotation])),  # Middle
            self.ml_place(rotate(shape, [0, 0, self.thumb_plate_ml_rotation])),  # Left
        ])

    # ============================================================================
    # Thumb Generation
    # ============================================================================

    def thumbcaps(self, side='right'):
        """Generate thumb keycaps."""
        return self.thumb_15x_layout(sa_cap())

    def thumb(self, side="right"):
        """Generate the complete thumb cluster."""
        print('thumb()')
        shape = self.thumb_fx_layout(rotate(single_plate(side=side), [0.0, 0.0, -90]))
        shape = union([shape, self.thumb_fx_layout(adjustable_plate(self.minidox_Usize))])
        return shape

    # ============================================================================
    # Web Post Positions (for connectors)
    # ============================================================================

    def thumb_post_tr(self):
        """Top right post position."""
        debugprint('thumb_post_tr()')
        return translate(web_post(),
                        [(mount_width / 2) - post_adj,
                         ((mount_height / 2) + adjustable_plate_size(self.minidox_Usize)) - post_adj,
                         0])

    def thumb_post_tl(self):
        """Top left post position."""
        debugprint('thumb_post_tl()')
        return translate(web_post(),
                        [-(mount_width / 2) + post_adj,
                         ((mount_height / 2) + adjustable_plate_size(self.minidox_Usize)) - post_adj,
                         0])

    def thumb_post_bl(self):
        """Bottom left post position."""
        debugprint('thumb_post_bl()')
        return translate(web_post(),
                        [-(mount_width / 2) + post_adj,
                         -((mount_height / 2) + adjustable_plate_size(self.minidox_Usize)) + post_adj,
                         0])

    def thumb_post_br(self):
        """Bottom right post position."""
        debugprint('thumb_post_br()')
        return translate(web_post(),
                        [(mount_width / 2) - post_adj,
                         -((mount_height / 2) + adjustable_plate_size(self.minidox_Usize)) + post_adj,
                         0])

    # ============================================================================
    # Connectors and Walls
    # ============================================================================

    def thumb_connectors(self, side="right"):
        """Generate connectors between thumb keys and to main keyboard."""
        print('thumb_connectors()')
        hulls = []

        # Connect middle and right keys
        hulls.append(
            triangle_hulls([
                self.tl_place(self.thumb_post_tr()),  # Middle key
                self.tl_place(self.thumb_post_br()),
                self.tr_place(self.thumb_post_tl()),  # Right key
                self.tr_place(self.thumb_post_bl()),
            ])
        )

        # Connect left and middle keys
        hulls.append(
            triangle_hulls([
                self.tl_place(self.thumb_post_tl()),  # Middle key
                self.tl_place(self.thumb_post_bl()),
                self.ml_place(self.thumb_post_tr()),  # Left key
                self.ml_place(self.thumb_post_br()),
            ])
        )

        # Connect thumb cluster to main keyboard
        hulls.append(
            triangle_hulls([
                self.tl_place(self.thumb_post_tl()),
                cluster_key_place(web_post_bl(), 0, cornerrow),
                self.tl_place(self.thumb_post_tr()),
                cluster_key_place(web_post_br(), 0, cornerrow),
                self.tr_place(self.thumb_post_tl()),
                cluster_key_place(web_post_bl(), 1, cornerrow),
                self.tr_place(self.thumb_post_tr()),
                cluster_key_place(web_post_br(), 1, cornerrow),
                cluster_key_place(web_post_tl(), 2, lastrow),
                cluster_key_place(web_post_bl(), 2, lastrow),
                cluster_key_place(web_post_bl(), 2, lastrow),
                cluster_key_place(web_post_br(), 1, cornerrow),
                self.tr_place(self.thumb_post_tr()),
                cluster_key_place(web_post_bl(), 2, lastrow),
                self.tr_place(self.thumb_post_br()),
                self.tr_place(self.thumb_post_tr()),
                cluster_key_place(web_post_bl(), 2, lastrow),
                self.tr_place(self.thumb_post_br()),
                cluster_key_place(web_post_br(), 2, lastrow),
                cluster_key_place(web_post_bl(), 3, lastrow),
                cluster_key_place(web_post_tr(), 2, lastrow),
                cluster_key_place(web_post_tl(), 3, lastrow),
                cluster_key_place(web_post_bl(), 3, cornerrow),
                cluster_key_place(web_post_tr(), 3, lastrow),
                cluster_key_place(web_post_br(), 3, cornerrow),
            ])
        )

        hulls.append(
            triangle_hulls([
                cluster_key_place(web_post_tr(), 3, lastrow),
                cluster_key_place(web_post_br(), 3, lastrow),
                cluster_key_place(web_post_bl(), 4, cornerrow),
            ])
        )

        hulls.append(
            triangle_hulls([
                cluster_key_place(web_post_tr(), 3, lastrow),
                cluster_key_place(web_post_br(), 3, cornerrow),
                cluster_key_place(web_post_bl(), 4, cornerrow),
            ])
        )

        hulls.append(
            triangle_hulls([
                cluster_key_place(web_post_br(), 1, cornerrow),
                cluster_key_place(web_post_tl(), 2, lastrow),
                cluster_key_place(web_post_bl(), 2, cornerrow),
                cluster_key_place(web_post_tr(), 2, lastrow),
                cluster_key_place(web_post_br(), 2, cornerrow),
                cluster_key_place(web_post_bl(), 3, cornerrow),
            ])
        )

        return union(hulls)

    def walls(self, side="right"):
        """Generate walls around the thumb cluster."""
        print('thumb_walls()')

        shape = wall_brace(self.tr_place, 0, -1, self.thumb_post_br(),
                          self.tr_place, 0, -1, self.thumb_post_bl())
        shape = union([shape, wall_brace(self.tr_place, 0, -1, self.thumb_post_bl(),
                                         self.tl_place, 0, -1, self.thumb_post_br())])
        shape = union([shape, wall_brace(self.tl_place, 0, -1, self.thumb_post_br(),
                                         self.tl_place, 0, -1, self.thumb_post_bl())])
        shape = union([shape, wall_brace(self.tl_place, 0, -1, self.thumb_post_bl(),
                                         self.ml_place, -1, -1, self.thumb_post_br())])
        shape = union([shape, wall_brace(self.ml_place, -1, -1, self.thumb_post_br(),
                                         self.ml_place, 0, -1, self.thumb_post_bl())])
        shape = union([shape, wall_brace(self.ml_place, 0, -1, self.thumb_post_bl(),
                                         self.ml_place, -1, 0, self.thumb_post_bl())])

        # Corners
        shape = union([shape, wall_brace(self.ml_place, -1, 0, self.thumb_post_bl(),
                                         self.ml_place, -1, 0, self.thumb_post_tl())])
        shape = union([shape, wall_brace(self.ml_place, -1, 0, self.thumb_post_tl(),
                                         self.ml_place, 0, 1, self.thumb_post_tl())])

        # Tweeners
        shape = union([shape, wall_brace(self.ml_place, 0, 1, self.thumb_post_tr(),
                                         self.ml_place, 0, 1, self.thumb_post_tl())])
        shape = union([shape, wall_brace(self.tr_place, 0, -1, self.thumb_post_br(),
                                         (lambda sh: cluster_key_place(sh, 3, lastrow)),
                                         0, -1, web_post_bl())])

        return shape

    def connection(self, side='right'):
        """Generate connection between thumb cluster and main keyboard body."""
        print('thumb_connection()')

        shape = bottom_hull([
            left_cluster_key_place(translate(web_post(), wall_locate2(-1, 0)),
                                  cornerrow, -1, low_corner=True, side=side),
            left_cluster_key_place(translate(web_post(), wall_locate3(-1, 0)),
                                  cornerrow, -1, low_corner=True, side=side),
            self.bl_place(translate(self.thumb_post_tr(), wall_locate2(-0.3, 1))),
            self.bl_place(translate(self.thumb_post_tr(), wall_locate3(-0.3, 1))),
        ])

        shape = union([shape, hull_from_shapes([
            left_cluster_key_place(translate(web_post(), wall_locate2(-1, 0)),
                                  cornerrow, -1, low_corner=True, side=side),
            left_cluster_key_place(translate(web_post(), wall_locate3(-1, 0)),
                                  cornerrow, -1, low_corner=True, side=side),
            self.ml_place(translate(self.thumb_post_tr(), wall_locate2(-0.3, 1))),
            self.ml_place(translate(self.thumb_post_tr(), wall_locate3(-0.3, 1))),
            self.tl_place(self.thumb_post_tl()),
        ])])

        shape = union([shape, hull_from_shapes([
            left_cluster_key_place(web_post(), cornerrow, -1, low_corner=True, side=side),
            left_cluster_key_place(translate(web_post(), wall_locate1(-1, 0)),
                                  cornerrow, -1, low_corner=True, side=side),
            left_cluster_key_place(translate(web_post(), wall_locate2(-1, 0)),
                                  cornerrow, -1, low_corner=True, side=side),
            left_cluster_key_place(translate(web_post(), wall_locate3(-1, 0)),
                                  cornerrow, -1, low_corner=True, side=side),
            self.tl_place(self.thumb_post_tl()),
        ])])

        shape = union([shape, hull_from_shapes([
            left_cluster_key_place(web_post(), cornerrow, -1, low_corner=True, side=side),
            left_cluster_key_place(translate(web_post(), wall_locate1(-1, 0)),
                                  cornerrow, -1, low_corner=True, side=side),
            cluster_key_place(web_post_bl(), 0, cornerrow),
            self.tl_place(self.thumb_post_tl()),
        ])])

        shape = union([shape, hull_from_shapes([
            self.ml_place(self.thumb_post_tr()),
            self.ml_place(translate(self.thumb_post_tr(), wall_locate1(0, 1))),
            self.ml_place(translate(self.thumb_post_tr(), wall_locate2(0, 1))),
            self.ml_place(translate(self.thumb_post_tr(), wall_locate3(0, 1))),
            self.tl_place(self.thumb_post_tl()),
        ])])

        return shape

    def screw_positions(self):
        """Calculate screw hole positions for the thumb cluster."""
        position = self.thumborigin()
        position = list(np.array(position) + np.array([-37, -34, -16]))
        position[1] = position[1] - .4 * (self.minidox_Usize - 1.7) * sa_length
        position[2] = 0
        return position
