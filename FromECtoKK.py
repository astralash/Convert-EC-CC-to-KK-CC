
"""
Reference: https://github.com/great-majority/KoikatuCharaLoader/tree/master/samples

"""

import copy
import os
import sys
import time
import shutil
import datetime


from kkloader.KoikatuCharaData import KKEx
from kkloader.EmocreCharaData import EmocreCharaData  # noqa
from kkloader.KoikatuCharaData import Coordinate, KoikatuCharaData  # noqa


def Convert(ec, DstPath):
	kk = KoikatuCharaData()

	kk.image = ec.image
	kk.face_image = ec.image
	kk.product_no = 100
	kk.header = "【KoiKatuChara】".encode("utf-8")
	kk.version = "0.0.0".encode("ascii")
	kk.blockdata = copy.deepcopy(ec.blockdata)
	try:
		kk.blockdata.insert(-1, "KKEx")
	except Exception as e:
		print("Except A")
		print(e)	
		
	kk.Custom = copy.deepcopy(ec.Custom)
	kk.Coordinate = Coordinate(data=None, version="0.0.0")
	kk.Parameter = copy.deepcopy(ec.Parameter)
	kk.Status = copy.deepcopy(ec.Status)
	
	kk.Custom["face"]["version"] = "0.0.2"
	kk.Custom["face"]["pupilHeight"] *= 1.08
	
	
	try:
		kk.Custom["face"]["hlUpY"] = (kk.Custom["face"]["hlUpY"] - 0.25) * 2
	except Exception:
		kk.Custom["face"]["hlUpY"] = 0.5
	
	
	
	del kk.Custom["face"]["hlUpX"]
	del kk.Custom["face"]["hlDownX"]
	del kk.Custom["face"]["hlUpScale"]
	del kk.Custom["face"]["hlDownScale"]
	kk.Custom["body"]["version"] = "0.0.2"
	kk.Custom["hair"]["version"] = "0.0.4"

	ec.Coordinate["clothes"]["hideBraOpt"] = [False, False]
	ec.Coordinate["clothes"]["hideShortsOpt"] = [False, False]
	for i, p in enumerate(ec.Coordinate["clothes"]["parts"]):
		a = {
			"emblemeId": p["emblemeId"][0],
			"emblemeId2": p["emblemeId"][1],
		}
		ec.Coordinate["clothes"]["parts"][i].update(a)
	ec.Coordinate["clothes"]["parts"].append(ec.Coordinate["clothes"]["parts"][-1])
	for i, a in enumerate(ec.Coordinate["accessory"]["parts"]):
		del ec.Coordinate["accessory"]["parts"][i]["hideTiming"]
	makeup = copy.deepcopy(ec.Custom["face"]["baseMakeup"])
	kk.Coordinate.data = [
		{
			"clothes": ec.Coordinate["clothes"],
			"accessory": ec.Coordinate["accessory"],
			"enableMakeup": False,
			"makeup": makeup,
		}
	] * 7

	kk.Parameter["version"] = "0.0.5"
	kk.Parameter["lastname"] = " "
	kk.Parameter["firstname"] = ec.Parameter["fullname"]
	kk.Parameter["nickname"] = " "
	kk.Parameter["callType"] = -1
	kk.Parameter["clubActivities"] = 0
	kk.Parameter["weakPoint"] = 0
	items = [
		"animal",
		"eat",
		"cook",
		"exercise",
		"study",
		"fashionable",
		"blackCoffee",
		"spicy",
		"sweet",
	]
	kk.Parameter["awnser"] = dict.fromkeys(items, True)
	items = ["kiss", "aibu", "anal", "massage", "notCondom"]
	kk.Parameter["denial"] = dict.fromkeys(items, False)
	items = [
		"hinnyo",
		"harapeko",
		"donkan",
		"choroi",
		"bitch",
		"mutturi",
		"dokusyo",
		"ongaku",
		"kappatu",
		"ukemi",
		"friendly",
		"kireizuki",
		"taida",
		"sinsyutu",
		"hitori",
		"undo",
		"majime",
		"likeGirls",
	]
	kk.Parameter["attribute"] = dict.fromkeys(items, True)
	kk.Parameter["aggressive"] = 0
	kk.Parameter["diligence"] = 0
	kk.Parameter["kindness"] = 0
	del kk.Parameter["fullname"]
	kk.Parameter["personality"] = 0

	kk.Status["version"] = "0.0.0"
	kk.Status["clothesState"] = b"\x00" * 9
	kk.Status["eyesBlink"] = False
	kk.Status["mouthPtn"] = 1
	kk.Status["mouthOpenMax"] = 0
	kk.Status["mouthFixed"] = True
	kk.Status["eyesLookPtn"] = 1
	kk.Status["neckLookPtn"] = 3
	kk.Status["visibleSonAlways"] = False
	del kk.Status["mouthOpenMin"]
	del kk.Status["enableSonDirection"]
	del kk.Status["sonDirectionX"]
	del kk.Status["sonDirectionY"]
	kk.Status["coordinateType"] = 4
	kk.Status["backCoordinateType"] = 0
	kk.Status["shoesType"] = 1
	
	if hasattr(ec, "KKEx"):
		kk.KKEx = ec.KKEx
	else:
		kk.KKEx = KKEx(data=" ".encode("utf-8"), version="3")

	kk.save(DstPath)



	
def main():
	PNGNum = 0
	CCNum = 0
	ChangedNum = 0
	Root = "."
	InitTime = time.perf_counter()
	LastTime = InitTime
	
	ConvertedDirPrefix = "ConvertedFromECtoKK"
	ConvertedDirName = ConvertedDirPrefix + str(datetime.datetime.now()).replace(":", "-") 
	ConvertedPath = os.path.join(Root, ConvertedDirName)
	
	for dirpath, dirnames, filenames in os.walk(Root):
		if ConvertedDirPrefix in dirpath:
			continue
		NewPath = dirpath.replace(Root, ConvertedPath, 1)
		for FileName in filenames:
			if FileName.endswith('.png'):
				PNGNum += 1
				TotalFilePath = os.path.join(dirpath, FileName)
				try:
					ec = EmocreCharaData.load(TotalFilePath)
					
					if (not hasattr(ec, "Custom")):
						continue
					
					if (not hasattr(ec, "Parameter")):
						continue
					
					try:
						ec.Parameter["fullname"]
					except Exception as e:
						continue
					
					os.makedirs(name = NewPath, exist_ok = True)
					CCNum += 1	
					Convert(ec, os.path.join(NewPath, FileName))
					
				except Exception as e:
					pass
		if time.perf_counter() - LastTime > 10 :
			LastTime = time.perf_counter()
			print("Run " + str(LastTime - InitTime) + " seconds:")
			print("PNGNum: " + str(PNGNum))
			print("EcCCNum: " + str(CCNum))
			print("")
	
	print("Runs " + str(time.perf_counter() - InitTime) + " seconds:")
	print("PNGNum: " + str(PNGNum))
	print("EcCCNum: " + str(CCNum))
	print("")
	

	os.system('pause')	

if __name__ == "__main__":
	main()
