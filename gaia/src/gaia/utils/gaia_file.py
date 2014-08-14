import os

class GaiaFile(file):
    ' A GaiaFile is a file with some standardised naming convenience functions/attribute. '
    image_types     = ['jpg', 'png', 'jpeg', 'tif', 'tiff']  # 'gif', 'bmp']
    web_image_types = ['jpg', 'png', 'jpeg',]                # 'gif']
    audio_types = ['mp3', ] 
    video_types = ['mp4', ]     # TODO...not yet used.

    @property
    def fpath(self):
        return self.name

    @property
    def fname(self):
        return os.path.basename(self.name)

    @property
    def ftype(self):
        name, ext =  os.path.splitext(self.name)
        if ext.startswith('.'):
            return ext[1:]  # eg change ".jpg' to 'jpg'
        else:
            return ext # presumably '' (for a file with no extension, eg 'do_it' or '.cshrc')

    @property
    def fbase(self):
        ''' return the fname of this asset _without_ the extension.
        
            eg foo for /x/y/z/foo.png
            similar to unix basename command with a suffix option
        '''
        # Note: we can't use "name" unfortunately as it's the fname and required for file() compatibility.
        name, ext =  os.path.splitext(self.name)
        return os.path.basename(name)

    # WARNING: these is_ methods will need extending, but this is all we need for now I think.
    def is_image(self):
        return self.ftype.lower() in self.image_types

    def is_web_image(self):
        ' is this file a web-displayable image '
        return self.ftype.lower() in self.web_image_types
                
    def is_audio(self):
        return self.ftype.lower() in self.audio_types

    def is_video(self):
        return self.ftype.lower() in self.video_types
