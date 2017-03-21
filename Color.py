from wox import Wox
import os
import tempfile

class HelloWorld(Wox):

    def query(self, query):
        params = query.split(" ")
        color = "Query: {}".format(query)
        icon = "Images/app.png"
        if len(params) == 3 or len(params) == 4:
            color = 0
            shift = 0
            params.reverse()
            for item in params:
                color += int(item) << shift
                shift = shift + 8
            color = hex(color).replace("0x", "#")
            # icon = createColorThumb(int(params[2]), int(params[1]), int(params[0]))
        results = []
        results.append({
            "Title": color,
            "SubTitle": "Copy to clipboard",
            "IcoPath": icon,
            'JsonRPCAction':{
                    'method': 'copy_colorHex',
                    'parameters': [color],
                    'dontHideAfterAction': False
                    }
        })
        return results

    def copy_colorHex(self, color):
            command = 'echo ' + color.strip() + '| clip'
            os.system(command)

    # def createColorThumb(r, b, g):
    #     img = Image.new('RGB', (100, 100), (r, b, g))
    #     tf = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    #     img.save(tf.name)
    #     return tf.name

if __name__ == "__main__":
    HelloWorld()
